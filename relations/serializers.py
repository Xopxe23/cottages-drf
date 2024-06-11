from rest_framework import serializers

from cottages.serializers import CottageCreateUpdateSerializer
from relations.models import UserCottageRent, UserCottageReview
from users.serializers import UserFullNameSerializer


class UserCottageReviewSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = UserCottageReview
        fields = ['id', 'user', "location_rating", "cleanliness_rating", "communication_rating",
                  "value_rating", "comment", "rating"]
        read_only_fields = ["rating", "user"]

    def to_internal_value(self, data):
        if self.instance:
            for field in ['location_rating', 'cleanliness_rating', 'communication_rating', 'value_rating', 'comment']:
                self.fields[field].required = False
        return super().to_internal_value(data)


class UserCottageRentSerializer(serializers.ModelSerializer):
    cottage = CottageCreateUpdateSerializer(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    # noinspection PyMethodMayBeStatic
    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = UserCottageRent
        fields = ['id', "start_date", "end_date", "status", "cottage"]
