from uuid import UUID

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cottages.models import Cottage
from cottages.permissions import IsAuthorOrReadOnly
from cottages.serializers import CottageCreateUpdateSerializer, CottageInfoWithRatingSerializer
from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.tasks import schedule_check_and_update_payment_status
from relations.models import UserCottageLike, UserCottageRent, UserCottageReview
from relations.serializers import UserCottageRentSerializer, UserCottageReviewSerializer


class UserCottageReviewList(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, cottage_id: UUID) -> Response:
        queryset = UserCottageReview.objects.filter(cottage_id=cottage_id).select_related("user")
        serializer = UserCottageReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def post(self, request: Request, cottage_id: UUID) -> Response:
        serializer = UserCottageReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, cottage_id=cottage_id)
            data = {'status': 'Cottage review created successfully', 'data': serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCottageReviewDetail(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    # noinspection PyMethodMayBeStatic
    def get_object(self, review_id: UUID):
        try:
            return UserCottageReview.objects.select_related("user").get(pk=review_id)
        except UserCottageReview.DoesNotExist:
            raise Http404

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, cottage_id: UUID, review_id: UUID) -> Response:
        review = self.get_object(review_id)
        serializer = UserCottageReviewSerializer(review)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def put(self, request: Request, cottage_id: UUID, review_id: UUID) -> Response:
        review = self.get_object(review_id)
        serializer = UserCottageReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {'status': 'Cottage review updated successfully', 'data': serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # noinspection PyMethodMayBeStatic
    def delete(self, request: Request, cottage_id: UUID, review_id: UUID) -> Response:
        review = self.get_object(review_id)
        review.delete()
        return Response({'status': 'Cottage review deleted successfully'}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cottage_rent_view(request: Request, cottage_id: UUID) -> Response:
    serializer = UserCottageRentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['start_date']
    end_date = serializer.validated_data['end_date']
    cottage = Cottage.objects.filter(pk=cottage_id).prefetch_related('rents').first()
    if not cottage:
        raise Http404("Cottage does not exist")
    if cottage.is_available(start_date, end_date):
        rent = serializer.save(user=request.user, cottage_id=cottage_id, status=1)
        payment = Payment.objects.create_payment(rent)
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
    serializer = CottageCreateUpdateSerializer(cottages, many=True)
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
    liked_cottages_list_id = UserCottageLike.objects.filter(user=user).values_list('cottage_id', flat=True)
    liked_cottages = Cottage.objects.get_cottages_list().filter(id__in=liked_cottages_list_id)
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
