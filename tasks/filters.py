from django_filters import FilterSet, CharFilter

from tasks.models import Task


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = ["status", "priority", "assigned_to_id", "created_by__id"]
