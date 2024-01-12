from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from towns.models import Town, TownAttraction
from towns.permissions import IsAdminOrReadOnly
from towns.serializers import TownAttractionSerializer, TownSerializer


@swagger_auto_schema(tags=['Towns'])
class TownViewSet(viewsets.ModelViewSet):
    queryset = Town.objects.prefetch_related("images", "attractions")
    serializer_class = TownSerializer
    permission_classes = [IsAdminOrReadOnly]


class TownAttractionViewSet(viewsets.ModelViewSet):
    serializer_class = TownAttractionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        town_id = self.kwargs.get('town_pk')
        return TownAttraction.objects.filter(town__id=town_id)

    def perform_create(self, serializer):
        town_id = self.kwargs.get('town_pk')
        serializer.save(town_id=town_id)
