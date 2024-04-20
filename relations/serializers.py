from rest_framework import serializers

from cottages.serializers import CottageCreateSerializer
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
    cottage = CottageCreateSerializer(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = UserCottageRent
        fields = ['id', "start_date", "end_date", "status", "cottage"]
