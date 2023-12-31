from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from clients.filters import UserFilter
from clients.models import User
from clients.models.user import EmployeeAttendance
from clients.serializers import (
    UserSerializer,
    ReadUserDataSerializer,
    EmployeeAttendanceSerializer,
)


class UserViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UserFilter
    search_fields = ["id", "first_name", "last_name", "mobile"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadUserDataSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.has_perm("view_user"):
            return User.objects.filter(is_safe_deleted=False)
        else:
            return User.objects.filter(id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeAttendanceViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = EmployeeAttendanceSerializer
    queryset = EmployeeAttendance.objects.filter(is_safe_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
