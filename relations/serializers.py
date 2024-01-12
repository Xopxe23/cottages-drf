from rest_framework import serializers

from relations.models import UserCottageReview
from users.serializers import UserFullNameSerializer


class UserCottageReviewSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = UserCottageReview
        fields = ['id', 'user', "cottage_rating", "cleanliness_rating", "owner_rating", "comment"]
