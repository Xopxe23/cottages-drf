from django.db.models import Avg, Prefetch
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cottages.models import Cottage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import (
    CottageCreateSerializer,
    CottageDetailSerializer,
    CottageListSerializer,
    UserCottageReviewSerializer,
)
from relations.models import UserCottageReview


class CreateCottageView(generics.CreateAPIView):
    serializer_class = CottageCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            data = {'message': 'Cottage created successfully', 'data': response.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCottageView(generics.ListAPIView):
    serializer_class = CottageListSerializer
    queryset = Cottage.objects.select_related("category", "town").only(
        "town__name", "category__name", "name", "price", "beds", "guests", "rooms", "total_area", "images"
    ).prefetch_related(
        "images",
        Prefetch("reviews", queryset=UserCottageReview.objects.only(
            "cottage", "cottage_rating"))
    ).annotate(average_cottage_rating=Round(Avg("reviews__cottage_rating"), 1))
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name"]
    ordering_fields = ["price", "average_cottage_rating"]
    ordering = ["-average_cottage_rating"]
    permission_classes = [IsOwnerOrReadOnly]


class RetrieveUpdateDestroyCottageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CottageDetailSerializer
    queryset = Cottage.objects.select_related("town", "category").only(
        "category__name", "town__name", "name", "description", "address", "price", "guests", "beds", "rooms",
        "total_area", "latitude", "longitude"
    ).prefetch_related(
        "images", "rules",
        Prefetch("reviews", queryset=UserCottageReview.objects.select_related("user"))
    ).annotate(
        average_cottage_rating=Round(Avg("reviews__cottage_rating"), 1),
        average_cleanliness_rating=Round(Avg("reviews__cleanliness_rating"), 1),
        average_owner_rating=Round(Avg("reviews__owner_rating"), 1),
    ).all()
    permission_classes = [IsOwnerOrReadOnly]


class ListUserCottageReviewView(generics.ListCreateAPIView):
    serializer_class = UserCottageReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        cottage_id = self.kwargs['cottage_id']
        queryset = UserCottageReview.objects.filter(cottage_id=cottage_id).select_related("user").only(
            'id', 'user__first_name', "user__last_name", "cottage_rating",
            "comment", "cleanliness_rating", "owner_rating"
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, cottage_id=self.kwargs['cottage_id'])


class UpdateDestroyReviewView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = UserCottageReviewSerializer
    queryset = UserCottageReview.objects.select_related("user").only(
        'user__first_name', "user__last_name", "cottage_rating", "comment", "cleanliness_rating", "owner_rating"
    )
    permission_classes = [IsOwnerOrReadOnly]
