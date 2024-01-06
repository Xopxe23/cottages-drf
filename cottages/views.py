from django.db.models import Avg, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cottages.models import Cottage, CottageComment, CottageImage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import CottageSerializer


class CreateCottageView(generics.CreateAPIView):
    serializer_class = CottageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            data = {'message': 'Cottage created successfully', 'data': response.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        tags=["Cottages"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the cottage'),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the cottage'),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the cottage'),
                'options': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pool': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the cottage has a pool'),
                        'parking': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                  description='Whether parking is available'),
                        'air_conditioning': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                           description='Whether the cottage has air conditioning'),
                        'wifi': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether WiFi is available'),
                    },
                    description='Options for the cottage'
                ),
            },
            required=['address', 'latitude', 'longitude'],
        ),
        responses={
            201: openapi.Response('Cottage created successfully', CottageSerializer),
            400: 'Bad request if validation fails',
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new cottage.

        :return: A success message if cottage creation is successful.
        :rtype: dict
        """
        return self.create(request, *args, **kwargs)


class ListCottagesView(generics.ListAPIView):
    serializer_class = CottageSerializer
    queryset = Cottage.objects.select_related("owner").only(
        'id', 'owner__first_name', "owner__last_name", 'address', "price",
        'latitude', 'longitude', 'options', "images", "comments"
    ).prefetch_related(
        Prefetch("images", queryset=CottageImage.objects.only("cottage", "image")),
        Prefetch("comments", queryset=CottageComment.objects.select_related("user").only(
            "id", 'user__first_name', "user__last_name", "rating", "comment", "cottage"
        ))
    ).annotate(average_rating=Avg('comments__rating')).all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["address"]
    ordering_fields = ["price", "average_rating"]
    ordering = ["-average_rating"]

    @swagger_auto_schema(
        responses={200: CottageSerializer(many=True)},
        tags=["Cottages"]
    )
    def get(self, request, *args, **kwargs):
        """
        Return all cottages.

        :return: List of cottages.
        :rtype: rest_framework.response.Response
        """

        return super().get(request, *args, **kwargs)


class RetrieveUpdateCottageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CottageSerializer
    queryset = Cottage.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        responses={200: CottageSerializer()},
        tags=["Cottages"]
    )
    def get(self, request, *args, **kwargs):
        """
        Return cottage by UUID.

        :return: List of cottages.
        :rtype: list
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the cottage'),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the cottage'),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the cottage'),
                'options': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pool': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the cottage has a pool'),
                        'parking': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                  description='Whether parking is available'),
                        'air_conditioning': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                           description='Whether the cottage has air conditioning'),
                        'wifi': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether WiFi is available'),
                    },
                    description='Options for the cottage'
                ),
            },
            required=['address', 'latitude', 'longitude'],
        ),
        responses={200: CottageSerializer()},
        tags=["Cottages"],
    )
    def put(self, request, *args, **kwargs):
        """
        Update an existing cottage.

        :return: Updated cottage.
        :rtype: rest_framework.response.Response
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the cottage'),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the cottage'),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the cottage'),
                'options': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pool': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the cottage has a pool'),
                        'parking': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                  description='Whether parking is available'),
                        'air_conditioning': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                           description='Whether the cottage has air conditioning'),
                        'wifi': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether WiFi is available'),
                    },
                    description='Options for the cottage'
                ),
            },
            required=['address', 'latitude', 'longitude'],
        ),
        responses={200: CottageSerializer()},
        tags=["Cottages"],
    )
    def patch(self, request, *args, **kwargs):
        """
        Update an existing cottage partially.

        :return: Partially updated cottage.
        :rtype: rest_framework.response.Response
        """
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: 'No Content'},
        tags=["Cottages"]
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing cottage.

        :return: No content.
        :rtype: rest_framework.response.Response
        """
        return super().delete(request, *args, **kwargs)
