from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer, ReadTaskSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_safe_deleted=False).order_by("-created_at")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = [
        "id",
        "title",
        "assigned_to__first_name",
        "assigned_to__last_name",
        "assigned_to__mobile",
        "created_by__first_name",
        "created_by__last_name",
        "created_by__mobile",
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.filter(is_safe_deleted=False)
        else:
            return Task.objects.filter(assigned_to=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadTaskSerializer
        return TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
