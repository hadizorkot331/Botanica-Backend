from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_plants_list_create_view, name='user-plants-list'),
    path('<int:pk>/', views.user_plants_detail_view, name='user-plants-detail'),
    path('<int:pk>/update/', views.user_plants_update_view, name='user-plants-update'),
    path('<int:pk>/delete/', views.user_plants_delete_view, name='user-plants-delete'),
]