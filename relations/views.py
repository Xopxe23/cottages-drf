from uuid import UUID

from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from cottages.models import Cottage
from cottages.permissions import IsAuthorOrReadOnly
from cottages.serializers import CottageCreateSerializer, CottageInfoWithRatingSerializer
from cottages.services import get_cottages_list
from payments.serializers import PaymentSerializer
from payments.services import create_payment
from payments.tasks import schedule_check_and_update_payment_status
from relations.models import UserCottageLike, UserCottageRent, UserCottageReview
from relations.serializers import UserCottageRentSerializer, UserCottageReviewSerializer
from relations.services import get_liked_cottages_ids, is_cottage_available


class ListUserCottageReviewView(generics.ListCreateAPIView):
    serializer_class = UserCottageReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet[UserCottageReview]:
        cottage_id = self.kwargs['cottage_id']
        queryset = UserCottageReview.objects.filter(cottage_id=cottage_id).select_related("user")
        return queryset

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user, cottage_id=self.kwargs['cottage_id'])


class UpdateDestroyReviewView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = UserCottageReviewSerializer
    queryset = UserCottageReview.objects.select_related("user")
    permission_classes = [IsAuthorOrReadOnly]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cottage_rent_view(request: Request, cottage_id: UUID) -> Response:
    serializer = UserCottageRentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['start_date']
    end_date = serializer.validated_data['end_date']

    if is_cottage_available(cottage_id, start_date, end_date):
        rent = serializer.save(user=request.user, cottage_id=cottage_id, status=1)
        payment = create_payment(rent, "localhost:8000/cottages")
        schedule_check_and_update_payment_status.delay(payment.id)
        payment_serializer = PaymentSerializer(payment)
        return Response({
            "status": "success",
            "data": payment_serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Коттедж занят в указанные даты"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_rents_view(request: Request) -> Response:
    user = request.user
    rents = UserCottageRent.objects.select_related("cottage").filter(user=user)
    serializer = UserCottageRentSerializer(rents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_cottages_view(request: Request) -> Response:
    user = request.user
    cottages = Cottage.objects.filter(owner=user)
    serializer = CottageCreateSerializer(cottages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_or_remove_favorites(request: Request, cottage_id: UUID) -> Response:
    user = request.user
    exists = UserCottageLike.objects.filter(user=user, cottage_id=cottage_id).first()
    if exists:
        exists.delete()
        return Response({"status": "removed from favorites"}, status=status.HTTP_200_OK)
    UserCottageLike.objects.create(user=user, cottage_id=cottage_id)
    return Response({"status": "cottage added to favorites"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_favorites(request: Request) -> Response:
    user = request.user
    liked_cottages_list_id = get_liked_cottages_ids(user)
    liked_cottages = get_cottages_list(pk__in=liked_cottages_list_id)
    serializer = CottageInfoWithRatingSerializer(liked_cottages, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cottage_to_favorites(request: Request, cottage_id: UUID) -> Response:
    user = request.user
    UserCottageLike.objects.create(user=user, cottage_id=cottage_id)
    return Response({"status": "cottage added to favorites"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_cottage_from_favorites(request: Request, cottage_id: UUID) -> Response:
    user = request.user
    UserCottageLike.objects.filter(user=user, cottage_id=cottage_id).delete()
    return Response({"status": "removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
