from django.urls.conf import path
from . import views

urlpatterns = [
    path("predict/", views.GetDataAPIView.as_view(), name="predict"),
    path("soil/", views.GetSoilDataAPIView.as_view(), name="soil"),
]
