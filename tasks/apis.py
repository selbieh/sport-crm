from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.serializers import TaskSerializer, ReadTaskSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadTaskSerializer
        return TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
