from datetime import datetime

from django.db.models import Avg, Max, Prefetch, Q
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cottages.models import Cottage, CottageImage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import (
    CottageCreateUpdateSerializer,
    CottageDetailUpdateSerializer,
    CottageListSerializer,
    ImageUpdateSerializer,
)
from relations.models import UserCottageRent, UserCottageReview
from relations.serializers import UserCottageReviewSerializer


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
        serializer.save(owner=self.request.user)


class ListCottageView(generics.ListAPIView):
    serializer_class = CottageListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name"]
    ordering_fields = ["price", "average_rating"]
    ordering = ["-average_rating"]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Cottage.objects.select_related("category", "town").prefetch_related("images", Prefetch(
            "reviews", queryset=UserCottageReview.objects.only("cottage", "cottage_rating"))
        ).annotate(average_rating=Round(Avg("reviews__cottage_rating"), 1))

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return queryset

            booked_cottages_subquery = UserCottageRent.objects.filter(
                Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[
                    start_date, end_date
                ]) | (Q(start_date__lte=start_date) & Q(end_date__gte=end_date))
            ).values_list('cottage')

            queryset = queryset.exclude(id__in=booked_cottages_subquery)

        return queryset


class RetrieveUpdateDestroyCottageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CottageDetailUpdateSerializer
    queryset = Cottage.objects.select_related("town", "category", "owner").prefetch_related("images").annotate(
        average_rating=Round(Avg("reviews__cottage_rating"), 1),
        average_cleanliness_rating=Round(Avg("reviews__cleanliness_rating"), 1),
        average_owner_rating=Round(Avg("reviews__owner_rating"), 1),
    ).all()
    permission_classes = [IsOwnerOrReadOnly]


class UpdateCottageImageOrder(APIView):

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
    def post(self, request, *args, **kwargs):
        serializer = ImageUpdateSerializer(data=request.data)
        if serializer.is_valid():
            image_id = serializer.validated_data.get("id")
            new_order = serializer.validated_data.get("order")
            try:
                image = CottageImage.objects.select_related('cottage').get(id=image_id)
            except CottageImage.DoesNotExist:
                return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
            max_order = image.cottage.images.aggregate(Max('order'))['order__max']
            if new_order > max_order:
                image.bottom()
            else:
                image.to(new_order)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "Order updated successfully"}, status=status.HTTP_200_OK)
