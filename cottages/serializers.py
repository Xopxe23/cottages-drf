from rest_framework import serializers

from cottages.models import Cottage, CottageAmenities, CottageCategory, CottageImage, CottageRules
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
    rules = CottageRulesSerializer()
    amenities = CottageAmenitiesSerializer()
    average_rating = serializers.FloatField(read_only=True)
    average_cleanliness_rating = serializers.FloatField(read_only=True)
    average_owner_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "owner", "rules", "amenities", "guests", "beds", "total_area", "rooms", "images",
            "average_rating", "average_cleanliness_rating", "average_owner_rating"
        ]

    def create(self, validated_data):
        rules_data = validated_data.pop('rules', {})
        amenities_data = validated_data.pop('amenities', {})

        cottage = Cottage.objects.create(**validated_data)

        CottageRules.objects.create(cottage=cottage, **rules_data)
        CottageAmenities.objects.create(cottage=cottage, **amenities_data)

        return cottage

    def update(self, instance, validated_data):
        rules_data = validated_data.pop('rules', {})
        amenities_data = validated_data.pop('amenities', {})

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        rules_instance, _ = CottageRules.objects.get_or_create(cottage=instance)
        for key, value in rules_data.items():
            setattr(rules_instance, key, value)
        rules_instance.save()

        amenities_instance, _ = CottageAmenities.objects.get_or_create(cottage=instance)
        for key, value in amenities_data.items():
            setattr(amenities_instance, key, value)
        amenities_instance.save()

        return instance


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
