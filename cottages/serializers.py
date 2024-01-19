from rest_framework import serializers

from cottages.models import Cottage, CottageCategory, CottageImage
from towns.serializers import TownNameSerializer
from users.serializers import UserFullNameSerializer


class CottageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageImage
        fields = ['id', 'image', 'order']


class CottageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageCategory
        fields = ["id", "name"]


class CottageListSerializer(serializers.ModelSerializer):
    images = CottageImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)

    class Meta:
        model = Cottage
        fields = ['id', 'town', 'category', "name", "price", "guests", "total_area",
                  "beds", "rooms", "average_rating", "images"]


class CottageCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    images = CottageImageSerializer(many=True, read_only=True)
    owner = UserFullNameSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    average_cleanliness_rating = serializers.FloatField(read_only=True)
    average_owner_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "owner", "guests", "beds", "total_area", "rooms", "images", "parking_places", "check_in_time",
            "check_out_time", "rules", "amenities", "average_rating", "average_cleanliness_rating",
            "average_owner_rating"
        ]


class CottageDetailUpdateSerializer(CottageCreateUpdateSerializer):
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)


class ImageUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    image = serializers.CharField(read_only=True)
    order = serializers.IntegerField()

    class Meta:
        model = CottageImage
        fields = ['id', 'image', 'order']

    def validate_order(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Order должен быть целым числом.")
        return value
