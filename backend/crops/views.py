from django.http import Http404
from rest_framework import authentication, generics, permissions
from rest_framework.exceptions import PermissionDenied

# Create your views here.

from .models import UserPlants
from .serializers import UserPlantsSerializer


class UserPlantsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserPlantsSerializer

    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlants.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


user_plants_list_create_view = UserPlantsListCreateAPIView.as_view()


class UserPlantsDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserPlantsSerializer

    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlants.objects.filter(user_id=self.request.user)

    def get_object(self):
        qs = self.get_queryset()
        obj = qs.filter(pk=self.kwargs['pk']).first()
        if not obj:
            raise Http404("Crop not found")
        return obj


user_plants_detail_view = UserPlantsDetailAPIView.as_view()


class UserPlantsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserPlantsSerializer

    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlants.objects.filter(user_id=self.request.user)

    def get_object(self):
        qs = self.get_queryset()
        obj = qs.filter(pk=self.kwargs['pk']).first()
        if not obj:
            raise Http404("Crop not found")
        return obj

    def perform_update(self, serializer):
        if serializer.instance.user_id != self.request.user:
            raise PermissionDenied("You don't have access to this plant")
        serializer.save(user_id=self.request.user)


user_plants_update_view = UserPlantsUpdateAPIView.as_view()


class UserPlantsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserPlantsSerializer

    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlants.objects.filter(user_id=self.request.user)

    def get_object(self):
        qs = self.get_queryset()
        obj = qs.filter(pk=self.kwargs['pk']).first()
        if not obj:
            raise Http404("Crop not found")
        return obj

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user:
            raise PermissionDenied("You don't have access to this plant")

        super().perform_destroy(instance)


user_plants_delete_view = UserPlantsDeleteAPIView.as_view()
