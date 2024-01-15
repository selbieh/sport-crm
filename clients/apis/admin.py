from django.contrib.auth.models import Group, Permission
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from clients.permissions import IsSystemAdmin
from clients.serializers import (
    GroupSerializer,
    ReadGroupsSerializer,
    ReadPermissionSerializer,
)


class RolesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsSystemAdmin]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadGroupsSerializer
        return GroupSerializer


class ListPermissionsApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]
    queryset = Permission.objects.all()
    serializer_class = ReadPermissionSerializer
