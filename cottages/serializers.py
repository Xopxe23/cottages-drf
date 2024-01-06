from rest_framework import serializers

from cottages.models import Cottage, CottageComment, CottageImage
from users.serializers import UserFullNameSerializer, UserSerializer


class CottageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageImage
        fields = ['image']


class CottageCommentSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer(read_only=True)

    class Meta:
        model = CottageComment
        fields = ['user', "rating", "comment"]


class CottageSerializer(serializers.ModelSerializer):
    owner = UserFullNameSerializer(read_only=True)
    id = serializers.CharField(read_only=True)
    images = CottageImageSerializer(many=True, read_only=True)
    comments = CottageCommentSerializer(many=True, read_only=True)
    # average_rating = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cottage
        fields = ['id', 'owner', 'address', "price", 'latitude', 'longitude',
                  'options', "average_rating", "images", "comments"]

    # def get_average_rating(self, obj):
    #     # obj - это экземпляр Cottage
    #     comments = obj.comments.all()
    #
    #     if comments:
    #         total_rating = sum(comment.rating for comment in comments)
    #         average_rating = total_rating / len(comments)
    #         return round(average_rating, 2)
    #     else:
    #         return None
