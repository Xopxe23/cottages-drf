from django.db.models import Max
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from cottages.serializers import ImageUpdateSerializer
from cottages.services import update_image_order
from towns.models import AttractionImage, Town, TownAttraction, TownImage
from towns.permissions import IsAdminOrReadOnly
from towns.serializers import TownAttractionSerializer, TownSerializer


@swagger_auto_schema(tags=['Towns'])
class TownViewSet(viewsets.ModelViewSet):
    queryset = Town.objects.prefetch_related("images", "attractions")
    serializer_class = TownSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TownAttractionViewSet(viewsets.ModelViewSet):
    queryset = TownAttraction.objects.prefetch_related("images")
    serializer_class = TownAttractionSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        town_id = self.kwargs.get('town_pk')
        return TownAttraction.objects.filter(town=town_id)

    def perform_create(self, serializer):
        town_id = self.kwargs.get('town_pk')
        serializer.save(town_id=town_id)


@api_view(['POST'])
@permission_classes(IsAdminOrReadOnly)
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING),
            'order': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['id', 'order'],
    ),
)
def update_town_image_order(request):
    serializer = ImageUpdateSerializer(data=request.data)
    if serializer.is_valid():
        image_id = serializer.validated_data.get("id")
        new_order = serializer.validated_data.get("order")
        try:
            image = TownImage.objects.select_related('town').get(id=image_id)
        except TownImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        max_order = image.town.images.aggregate(Max('order'))['order__max']
        update_image_order(image, new_order, max_order)
        return Response({"success": "Order updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(IsAdminOrReadOnly)
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING),
            'order': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['id', 'order'],
    ),
)
def update_attraction_image_order(request):
    serializer = ImageUpdateSerializer(data=request.data)
    if serializer.is_valid():
        image_id = serializer.validated_data.get("id")
        new_order = serializer.validated_data.get("order")
        try:
            image = AttractionImage.objects.select_related('attraction').get(id=image_id)
        except AttractionImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        max_order = image.attraction.images.aggregate(Max('order'))['order__max']
        update_image_order(image, new_order, max_order)
        return Response({"success": "Order updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
