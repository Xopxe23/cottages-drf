from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from cottages.permissions import IsOwnerOrReadOnly
from relations.models import UserCottageReview
from relations.serializers import UserCottageReviewSerializer


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
