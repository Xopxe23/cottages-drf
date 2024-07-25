from datetime import datetime
from uuid import UUID

from django.db.models import Max
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from elasticsearch_dsl.search_base import Request as ElasticRequest, Response as ElasticResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cottages.documents import CottageDocument, TownDocument
from cottages.models import Cottage, CottageImage
from cottages.permissions import IsOwnerOrReadOnly
from cottages.serializers import (
    CottageCreateUpdateSerializer,
    CottageDetailSerializer,
    CottageInfoWithRatingSerializer,
    ImageUpdateSerializer,
)


class CottageList(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name", "price", "average_rating"]
    ordering_fields = ["price", "average_rating"]
    ordering = ["-average_rating"]

    def get_queryset(self):
        pass

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request) -> Response:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Cottage.objects.get_cottages_list(start_date=start_date, end_date=end_date)
        serializer = CottageInfoWithRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> Response:
        serializer = CottageCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            cottage = serializer.save(owner=request.user)
            data = {'status': 'Cottage created successfully', 'data': serializer.data}
            data['data']['id'] = cottage.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CottageDetail(APIView):

    # noinspection PyMethodMayBeStatic
    def get_object(self, cottage_id: UUID) -> Cottage:
        try:
            return Cottage.objects.get(pk=cottage_id)
        except Cottage.DoesNotExist:
            raise Http404

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, cottage_id: UUID) -> Response:
        cottage = Cottage.objects.get_cottage_by_id(cottage_id)
        if cottage is None:
            raise Http404("Cottage does not exist")
        serializer = CottageDetailSerializer(instance=cottage)
        return Response(serializer.data)

    def put(self, request: Request, cottage_id: UUID) -> Response:
        cottage = self.get_object(cottage_id)
        serializer = CottageCreateUpdateSerializer(cottage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {'status': 'Cottage updated successfully', 'data': serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, cottage_id: UUID) -> Response:
        cottage = self.get_object(cottage_id)
        cottage.delete()
        return Response({'status': 'Cottage deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def cottage_search(request):
    query = request.query_params.get('query', '')
    search = CottageDocument.search().query("multi_match", query=query, fields=['name', 'town.name'])
    response = search.execute()
    cottage_ids = [hit.id for hit in response]
    cottages = Cottage.objects.get_cottages_list().filter(id__in=cottage_ids)
    serializer = CottageInfoWithRatingSerializer(cottages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def cottage_suggest(request):
    query = request.query_params.get('query', '')

    search: Search = CottageDocument.search()
    suggest: Search = search.suggest('name_suggestions', query, completion={'field': 'name.suggest'})
    suggest: Search = suggest.suggest('town_name_suggestions', query, completion={'field': 'town_name.suggest'})
    response: ElasticResponse = suggest.execute()
    cottage_name_suggestions = [
        {
            'id': option._source.id,
            'name': option._source.name,
            'town_name': option._source.town_name
        }
        for option in response.suggest.name_suggestions[0].options
    ]

    cottage_town_suggestions = [
        {
            'id': option._source.id,
            'name': option._source.name,
            'town_name': option._source.town_name
        }
        for option in response.suggest.town_name_suggestions[0].options
    ]
    cottage_suggestions = cottage_name_suggestions + cottage_town_suggestions
    search = TownDocument.search()
    suggest: Search = search.suggest('name_suggestions', query, completion={'field': 'name.suggest'})
    response: ElasticResponse = suggest.execute()
    town_suggestions = [
        {
            'id': option._source.id,
            'name': option._source.name,
        }
        for option in response.suggest.name_suggestions[0].options
    ]
    data = {"cottages": cottage_suggestions, "towns": town_suggestions}
    return Response(data, status.HTTP_200_OK)


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
        if new_order > max_order:
            image.bottom()
        else:
            image.to(new_order)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"success": "Order updated successfully"}, status=status.HTTP_200_OK)
