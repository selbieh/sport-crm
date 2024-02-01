from django_filters import FilterSet

from subscriptions.models import Subscription


class HomeDashboardExpirationFilter(FilterSet):
    class Meta:
        model = Subscription
        fields = ["plan_id", "user_id", "sales_person__id", "plan__duration_type"]
