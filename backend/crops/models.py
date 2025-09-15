from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from datetime import datetime


# Create your models here.


class Crop(models.Model):
    name = models.CharField(max_length=200)
    crop_yield = models.DecimalField(decimal_places=2, max_digits=100)
    indoor = models.BooleanField(null=True)
    cycle = models.CharField(max_length=200)
    watering = models.CharField(max_length=200)
    watering_avg_volume_requirement = models.IntegerField(null=True)
    pruning_month = models.CharField(null=True, max_length=200)
    growth_rate = models.CharField(null=True, max_length=200)
    min_hardiness = models.IntegerField(null=True)
    max_hardiness = models.IntegerField(null=True)
    image_url = models.URLField(null=True)
    sunlight = models.CharField(null=True, max_length=200)
    days_to_yield = models.IntegerField(default=100, null=False)

    def __str__(self):
        return self.name


class UserPlants(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_id = models.ForeignKey(Crop, on_delete=models.CASCADE)
    time_planted = models.DateTimeField(auto_now_add=True)
    last_watered = models.DateTimeField(auto_now=True)
    prediction_probability = models.FloatField()
    lon = models.DecimalField(max_digits=100, decimal_places=10)
    lat = models.DecimalField(max_digits=100, decimal_places=10)

    def clean(self):
        if self.last_watered < self.time_planted:
            raise ValidationError("Plant cannot be watered before planting time")
        if self.last_watered > datetime.now():
            raise ValidationError("Plant cannot be watered in the future")

        if not self.crop_id:
            raise ValidationError("Crop does not exist")
        if not self.user_id:
            raise ValidationError("User does not exist")

        return super().clean()

    def __str__(self):
        return f"""
            User: {self.user_id.username}
            Crop: {self.crop_id.name}
            """
