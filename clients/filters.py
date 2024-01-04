from django_filters import FilterSet, CharFilter

from clients.models import User


class UserFilter(FilterSet):
    group = CharFilter(field_name="groups__name", lookup_expr="contains")

    class Meta:
        model = User
        fields = [
            "group",
        ]
