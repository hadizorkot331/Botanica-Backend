from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS

from crops.models import Crop, UserPlants


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ALL_FIELDS

class UserPlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlants
        fields = ALL_FIELDS