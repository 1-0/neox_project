from rest_auth import serializers
from rest_framework import serializers as rf_serializers
from neox_project.models import CustomUser
from post import models


class PostSerializer(serializers.JWTSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = (
            'id',
            'title',
            'user',
            'content',
            'pub_date',
        )
        model = models.Post


class RatingSerializer(rf_serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = (
            'id',
            'like',
            'user',
            'post',
        )
        model = models.Rating


class UserActivitySerializer(serializers.JWTSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = (
            'id',
            'username',
            'date_joined',
        )
        model = CustomUser


class UserSerializer(rf_serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
