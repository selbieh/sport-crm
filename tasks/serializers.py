from rest_framework import serializers

from clients.serializers import ReadUserDataSerializer
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("is_safe_deleted",)


class ReadTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    details = serializers.CharField()
    assigned_to = ReadUserDataSerializer()
    deadline = serializers.DateField()
    reminder_intervals = serializers.CharField()
    status = serializers.CharField()
    priority = serializers.CharField()
    feedback = serializers.CharField()
    created_at = serializers.DateTimeField()
