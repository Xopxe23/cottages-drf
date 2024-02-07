from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from cottages.permissions import IsAuthorOrReadOnly
from relations.models import UserCottageReview
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


class CreateUserCottageRent(generics.CreateAPIView):
    serializer_class = UserCottageRentSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        user = self.request.user
        cottage_id = self.kwargs.get('cottage_id')
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        if is_cottage_available(cottage_id, start_date, end_date):
            serializer.save(user=user, cottage_id=cottage_id)
        else:
            raise ValidationError("Коттедж занят в указанный период")
