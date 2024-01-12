from django.db.models import Avg, Prefetch
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cottages.models import Cottage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import CottageCreateUpdateSerializer, CottageDetailUpdateSerializer, CottageListSerializer
from relations.models import UserCottageReview


class CreateCottageView(generics.CreateAPIView):
    serializer_class = CottageCreateUpdateSerializer
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
    serializer_class = CottageDetailUpdateSerializer
    queryset = Cottage.objects.select_related("town", "category").only(
        "category__name", "town__name", "name", "description", "address", "price", "guests", "beds", "rooms",
        "total_area", "latitude", "longitude"
    ).prefetch_related(
        "images", "rules", "amenities"
    ).annotate(
        average_cottage_rating=Round(Avg("reviews__cottage_rating"), 1),
        average_cleanliness_rating=Round(Avg("reviews__cleanliness_rating"), 1),
        average_owner_rating=Round(Avg("reviews__owner_rating"), 1),
    ).all()
    permission_classes = [IsOwnerOrReadOnly]
