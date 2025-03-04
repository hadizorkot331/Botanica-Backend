from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS

from crops.models import Crop, UserPlants


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ALL_FIELDS


class UserPlantsSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user_id", read_only=True)
    crop = CropSerializer(source="crop_id", read_only=True)

    class Meta:
        model = UserPlants

        fields = [
            'id',
            'user_id',
            'user',
            'crop_id',
            'crop',
            'time_planted',
            'last_watered',
            'prediction_probability',
            'lon',
            'lat',
        ]

        read_only_fields = ['time_planted']