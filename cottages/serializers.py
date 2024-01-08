from rest_framework import serializers

from cottages.models import Cottage, CottageAmenities, CottageCategory, CottageImage, CottageRules
from relations.models import UserCottageReview
from towns.serializers import TownNameSerializer
from users.serializers import UserFullNameSerializer


class CottageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageImage
        fields = ['image']


class CottageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageCategory
        fields = ["id", "name"]


class CottageReviewSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = UserCottageReview
        fields = ['user', "cottage_rating", "cleanliness_rating", "owner_rating", "comment"]


class CottageRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageRules
        fields = ["check_in_time", "check_out_time", "with_children",
                  "with_pets", "smoking", "parties", "need_documents"]


class CottageAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageAmenities
        fields = ["parking_spaces", "wifi", "tv", "air_conditioner", "hair_dryer", "electric_kettle"]


class CottageListSerializer(serializers.ModelSerializer):
    images = CottageImageSerializer(many=True, read_only=True)
    average_cottage_rating = serializers.FloatField(read_only=True)
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)

    class Meta:
        model = Cottage
        fields = ['id', 'town', 'category', "name", "price", "guests", "total_area",
                  "beds", "rooms", "average_cottage_rating", "images"]


class CottageDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    images = CottageImageSerializer(many=True, read_only=True)
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)
    user = UserFullNameSerializer(read_only=True)
    rules = CottageRulesSerializer(read_only=True)
    amenities = CottageAmenitiesSerializer(read_only=True)
    reviews = CottageReviewSerializer(many=True, read_only=True)
    average_cottage_rating = serializers.FloatField(read_only=True)
    average_cleanliness_rating = serializers.FloatField(read_only=True)
    average_owner_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "user", "rules", "amenities", "guests", "beds", "total_area", "rooms", "reviews", "images",
            "average_cottage_rating", "average_cleanliness_rating", "average_owner_rating"
        ]
