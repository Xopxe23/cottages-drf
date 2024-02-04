from rest_framework import serializers

from relations.models import UserCottageRent, UserCottageReview
from users.serializers import UserFullNameSerializer


class UserCottageReviewSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = UserCottageReview
        fields = ['id', 'user', "location_rating", "cleanliness_rating", "communication_rating",
                  "value_rating", "comment", "rating"]
        read_only_fields = ["rating", "user"]


class UserCottageRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCottageRent
        fields = ["start_date", "end_date"]
