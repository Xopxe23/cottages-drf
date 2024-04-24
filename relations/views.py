from django.db.models import Avg, Prefetch, Subquery
from django.db.models.functions import Round
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cottages.models import Cottage
from cottages.permissions import IsAuthorOrReadOnly
from cottages.serializers import CottageCreateSerializer, CottageListSerializer
from relations.models import UserCottageLike, UserCottageRent, UserCottageReview
from relations.serializers import UserCottageRentSerializer, UserCottageReviewSerializer
from relations.services import is_cottage_available


class ListUserCottageReviewView(generics.ListCreateAPIView):
    serializer_class = UserCottageReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        cottage_id = self.kwargs['cottage_id']
        queryset = UserCottageReview.objects.filter(cottage_id=cottage_id).select_related("user")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, cottage_id=self.kwargs['cottage_id'])


class UpdateDestroyReviewView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = UserCottageReviewSerializer
    queryset = UserCottageReview.objects.select_related("user")
    permission_classes = [IsAuthorOrReadOnly]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_cottage_rent_view(request, cottage_id):
    serializer = UserCottageRentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['start_date']
    end_date = serializer.validated_data['end_date']

    if is_cottage_available(cottage_id, start_date, end_date):
        serializer.save(user=request.user, cottage_id=cottage_id, status=1)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Коттедж занят в указанные даты"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_rents_view(request):
    user = request.user
    rents = UserCottageRent.objects.select_related("cottage").filter(user=user)
    serializer = UserCottageRentSerializer(rents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_cottages_view(request):
    user = request.user
    cottages = Cottage.objects.filter(owner=user)
    serializer = CottageCreateSerializer(cottages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_or_remove_favorites(request, cottage_id):
    user = request.user
    exists = UserCottageLike.objects.filter(user=user, cottage_id=cottage_id).first()
    if exists:
        exists.delete()
        return Response({"status": "removed from favorites"}, status=status.HTTP_200_OK)
    UserCottageLike.objects.create(user=user, cottage_id=cottage_id)
    return Response({"status": "cottage added to favorites"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_favorites(request):
    user = request.user
    liked_cottages_list_id = UserCottageLike.objects.filter(user=user).values('cottage_id')
    liked_cottages = Cottage.objects.filter(pk__in=Subquery(liked_cottages_list_id)).select_related(
        "category", "town"
    ).prefetch_related("images", Prefetch("reviews", queryset=UserCottageReview.objects.only(
        "cottage", "rating"))).annotate(
        average_rating=Round(Avg("reviews__rating"), 1))
    serializer = CottageListSerializer(liked_cottages, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cottage_to_favorites(request, cottage_id):
    user = request.user
    UserCottageLike.objects.create(user=user, cottage_id=cottage_id)
    return Response({"status": "cottage added to favorites"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_cottage_from_favorites(request, cottage_id):
    user = request.user
    UserCottageLike.objects.filter(user=user, cottage_id=cottage_id).delete()
    return Response({"status": "removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
