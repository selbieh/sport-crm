from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from clients.models import User
from dashboard.filters import HomeDashboardExpirationFilter
from dashboard.serializers import (
    HomeDashboardExpirationSerializer,
    UserSubscriptionSerializer,
)
from leads.models import Lead
from subscriptions.models import Subscription
from subscriptions.utility import DAYS, SESSIONS


class HomeDashboardExpirationApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = HomeDashboardExpirationSerializer
    queryset = Subscription.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = HomeDashboardExpirationFilter
    search_fields = [
        "id",
        "user__first_name",
        "user__last_name",
        "user__mobile",
        "sales_person__first_name",
        "sales_person__last_name",
        "sales_person__mobile",
        "plan__name",
    ]

    def get_queryset(self):
        seven_days_from_now = timezone.now() + timezone.timedelta(days=7)
        return self.queryset.filter(
            end_date__range=[timezone.now(), seven_days_from_now]
        )


class HomeDashboardAnalyticsApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = None
    queryset = Subscription.objects.all()

    def get(self, request, *args, **kwargs):
        year = self.request.query_params.get("year")
        if not year:
            from rest_framework import serializers

            raise serializers.ValidationError("must provide year to get results")
        context = {
            "income_per_month": Subscription.objects.filter(created_at__year=year)
            .values(month=ExtractMonth("created_at"))
            .annotate(total_income=Sum("total_amount")),
            "loads": Lead.objects.all()
            .values("status")
            .annotate(total_leads=Count("id")),
            "members": User.objects.filter(groups__name="Member")
            .values("gender")
            .annotate(total_members=Count("id")),
        }
        return Response(context)


class HomeMemberShipSalesClassesApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = None
    queryset = Subscription.objects.all()

    def get(self, request, *args, **kwargs):
        subscriptions = (
            Subscription.objects.filter(plan__duration_type=DAYS)
            .values("user")
            .annotate(subscriptions_count=Count("id"), total_amount=Sum("total_amount"))
        )
        academy_classes = (
            Subscription.objects.filter(plan__duration_type=SESSIONS)
            .values("user")
            .annotate(subscriptions_count=Count("id"), total_amount=Sum("total_amount"))
        )
        context = {
            "membership": UserSubscriptionSerializer(subscriptions, many=True).data,
            "classes": UserSubscriptionSerializer(academy_classes, many=True).data,
        }
        return Response(context)
