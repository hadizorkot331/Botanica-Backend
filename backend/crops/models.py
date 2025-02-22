from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from datetime import datetime

from sklearn.gaussian_process.kernels import Product


# Create your models here.

class Crop(models.Model):
    api_id = models.IntegerField()
    name = models.CharField()
    _yield = models.DecimalField(decimal_places=2)
    indoor = models.BooleanField(null=True)
    cycle = models.CharField()
    watering = models.CharField()
    watering_avg_volume_requirement = models.IntegerField(null=True)
    pruning_month = models.CharField(null=True)
    growth_rate = models.CharField(null=True)
    min_hardiness = models.IntegerField(null=True)
    max_hardiness = models.IntegerField(null=True)
    image_url = models.CharField(null=True)
    sunlight = models.CharField(null=True)

    def __str__(self):
        return f"""Name: {self.name}
Yield: {self._yield}
Indoor: {self.indoor}
Cycle: {self.cycle}
Watering: {self.watering}
Watering Avg Volume Requirement: {self.watering_avg_volume_requirement} L
Pruning Month: {self.pruning_month}
Growth Rate: {self.growth_rate}
Min. Hardiness: {self.min_hardiness}
Max. Hardiness: {self.max_hardiness}
Sunlight: {self.sunlight}
"""

class UserPlants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    time_planted = models.DateTimeField(auto_now_add=True)
    last_watered = models.DateTimeField(auto_now=True)
    prediction_probability = models.FloatField()
    long = models.DecimalField()
    lat = models.DecimalField()

    def clean(self):
        if self.last_watered < self.time_planted:
            raise ValidationError("Plant cannot be watered before planting time")
        if self.last_watered > datetime.now():
            raise ValidationError("Plant cannot be watered in the future")

        if not self.crop:
            raise ValidationError("Crop does not exist")
        if not self.user:
            raise ValidationError("User does not exist")

        return super().clean()

    def __str__(self):
        return f"""User: {self.user.username}
Crop: {self.crop.name}
Prediction: {self.prediction_probability}
Time Planted: {self.time_planted}
Location: Longitude: {self.lat}, Latitude: {self.lat}
Last Watered: {self.last_watered}
"""