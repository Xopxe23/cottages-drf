from datetime import datetime
from uuid import UUID

from django.db.models import Avg, Max, QuerySet
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cottages.models import Cottage, CottageImage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import (
    CottageCreateUpdateSerializer,
    CottageDetailSerializer,
    CottageInfoWithRatingSerializer,
    ImageUpdateSerializer,
)
from cottages.services import get_booked_cottages_ids, get_cottages_list, update_image_order


class CottageViewSet(ViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name"]
    ordering_fields = ["price", "average_rating"]
    ordering = ["-average_rating"]

    # noinspection PyMethodMayBeStatic
    def list(self, request: Request) -> Response:
        queryset = get_cottages_list()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            booked_cottages = get_booked_cottages_ids(start_date, end_date)
            queryset = queryset.exclude(id__in=booked_cottages)

        serializer = CottageInfoWithRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CottageCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            cottage = serializer.save(owner=request.user)
            data = {'status': 'Cottage created successfully', 'data': serializer.data}
            data['data']['id'] = cottage.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    create.permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def update(self, request: Request, pk: UUID) -> Response:
        cottage = get_object_or_404(Cottage, pk=pk)
        serializer = CottageCreateUpdateSerializer(cottage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {'status': 'Cottage updated successfully', 'data': serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # noinspection PyMethodMayBeStatic
    def retrieve(self, request: Request, pk: UUID) -> Response:
        cottage = get_object_or_404(Cottage.objects.select_related("town", "category", "owner").prefetch_related(
            "images").annotate(
                average_rating=Coalesce(Avg("reviews__rating"), 0.0),
                average_location_rating=Coalesce(Avg("reviews__location_rating"), 0.0),
                average_cleanliness_rating=Coalesce(Avg("reviews__cleanliness_rating"), 0.0),
                average_communication_rating=Coalesce(Avg("reviews__communication_rating"), 0.0),
                average_value_rating=Coalesce(Avg("reviews__value_rating"), 0.0)
        ).all(), pk=pk)
        serializer = CottageDetailSerializer(instance=cottage)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def delete(self, request: Request, pk: UUID) -> Response:
        cottage = get_object_or_404(Cottage, pk=pk)
        cottage.delete()
        return Response({'status': 'Cottage deleted successfully'}, status=status.HTTP_200_OK)


# class ListCottageView(generics.ListAPIView):
#     serializer_class = CottageInfoWithRatingSerializer
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ["name"]
#     ordering_fields = ["price", "average_rating"]
#     ordering = ["-average_rating"]
#     permission_classes = [IsOwnerOrReadOnly]
#
#     def get_queryset(self) -> QuerySet[Cottage]:
#         queryset = get_cottages_list()
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')
#         if start_date and end_date:
#             try:
#                 datetime.strptime(start_date, '%Y-%m-%d')
#                 datetime.strptime(end_date, '%Y-%m-%d')
#             except ValueError:
#                 return queryset
#             booked_cottages = get_booked_cottages_ids(start_date, end_date)
#             queryset = queryset.exclude(id__in=booked_cottages)
#         return queryset
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_cottage_view(request: Request) -> Response:
#     serializer = CottageCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(owner=request.user)
#         data = {'status': 'Cottage created successfully', 'data': serializer.data}
#         return Response(data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['PUT', 'PATCH'])
# @permission_classes([IsOwnerOrReadOnly])
# def update_cottage_view(request: Request) -> Response:
#     id = request.data.pop("id")
#     serializer = CottageUpdateSerializer(data=request.data)
#     if serializer.is_valid():
#         Cottage.objects.filter(pk=id).update(**serializer.data)
#         data = {'status': 'Cottage updated successfully', 'data': serializer.data}
#         return Response(data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def retrieve_cottage_view(request: Request, pk: UUID):
#     cottage = get_object_or_404(Cottage.objects.select_related(
#     "town", "category", "owner").prefetch_related("images").annotate(
#             average_rating=Avg("reviews__rating"),
#             average_location_rating=Avg("reviews__location_rating"),
#             average_cleanliness_rating=Avg("reviews__cleanliness_rating"),
#             average_communication_rating=Avg("reviews__communication_rating"),
#             average_value_rating=Avg("reviews__value_rating"),
#         ).all(), pk=pk)
#     serializer = CottageDetailUpdateSerializer(instance=cottage)
#     return Response(serializer.data)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsOwnerOrReadOnly])
# def delete_cottage_view(request: Request, pk: UUID) -> Response:
#     cottage = get_object_or_404(Cottage, pk=pk)
#     cottage.delete()
#     return Response({'status': 'Cottage deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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
