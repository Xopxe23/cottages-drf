from datetime import datetime

from django.db.models import Avg, Max, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from cottages.models import Cottage, CottageImage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import (
    CottageCreateSerializer,
    CottageDetailUpdateSerializer,
    CottageInfoWithRatingSerializer,
    ImageUpdateSerializer,
)
from cottages.services import get_booked_cottages_ids, get_cottages_list, update_image_order


class CreateCottageView(generics.CreateAPIView):
    serializer_class = CottageCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            data = {'message': 'Cottage created successfully', 'data': response.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListCottageView(generics.ListAPIView):
    serializer_class = CottageInfoWithRatingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name"]
    ordering_fields = ["price", "average_rating"]
    ordering = ["-average_rating"]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[Cottage]:
        queryset = get_cottages_list()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return queryset
            booked_cottages = get_booked_cottages_ids(start_date, end_date)
            queryset = queryset.exclude(id__in=booked_cottages)
        return queryset


class RetrieveUpdateDestroyCottageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CottageDetailUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[Cottage]:
        queryset = Cottage.objects.select_related("town", "category", "owner").prefetch_related("images").annotate(
            average_rating=Avg("reviews__rating"),
            average_location_rating=Avg("reviews__location_rating"),
            average_cleanliness_rating=Avg("reviews__cleanliness_rating"),
            average_communication_rating=Avg("reviews__communication_rating"),
            average_value_rating=Avg("reviews__value_rating"),
        ).all()
        return queryset


@swagger_auto_schema(
    method="post",
    request_body=ImageUpdateSerializer,
)
@api_view(['POST'])
def update_cottage_image_order(request: Request, *args, **kwargs) -> Response:
    serializer = ImageUpdateSerializer(data=request.data)
    if serializer.is_valid():
        image_id = serializer.validated_data.get("id")
        new_order = serializer.validated_data.get("order")
        try:
            image = CottageImage.objects.select_related('cottage').get(id=image_id)
        except CottageImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        max_order = image.cottage.images.aggregate(Max('order'))['order__max']
        update_image_order(image, new_order, max_order)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"success": "Order updated successfully"}, status=status.HTTP_200_OK)
