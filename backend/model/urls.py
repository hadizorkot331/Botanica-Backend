from django.urls.conf import path
from . import views

urlpatterns = [
    path("predict/", views.PredictAPIView.as_view(), name="predict"),
]
