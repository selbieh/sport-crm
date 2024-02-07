from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from Academy_class.models import AcademyClass
from clients.models import User
from dashboard.filters import HomeDashboardExpirationFilter
from dashboard.serializers import (
    HomeDashboardExpirationSerializer,
    SalesSubscriptionSerializer,
    SalesClassSerializer,
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
        subscriptions = (
            Subscription.objects.filter(created_at__year=year)
            .values(month=ExtractMonth("created_at"))
            .annotate(total_income=Sum("total_amount"))
        )
        leads = (
            Lead.objects.filter(created_at__year=year)
            .values("status")
            .annotate(total_leads=Count("id"))
        )
        users = (
            User.objects.filter(groups__name="Member", created_at__year=year)
            .values("gender")
            .annotate(total_members=Count("id"))
        )
        context = {
            "income_per_month": subscriptions if subscriptions else 0,
            "loads": leads if leads else 0,
            "members": users if users else 0,
        }
        return Response(context)


class HomeMemberShipSalesSubscriptionApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SalesSubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return (
            Subscription.objects.filter(plan__duration_type=DAYS)
            .values("sales_person")
            .annotate(subscriptions_count=Count("id"), total_amount=Sum("total_amount"))
        )


class HomeMemberShipSalesClassApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SalesClassSerializer
    queryset = AcademyClass.objects.all()

    def get_queryset(self):
        return self.queryset.values("instructor").annotate(
            classes_count=Count("id"),
            total_amount=Sum("academy_class_attendance__subscription__total_amount"),
        )
