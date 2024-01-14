from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from subscriptions.models import (
    Package,
    Plan,
    Subscription,
    FreezingRequest,
    SubscriptionAttendance,
    WalkInType,
    WalkInUser,
)
from subscriptions.serializers import (
    PackagesSerializer,
    ReadPackageSerializer,
    PlanSerializer,
    ReadPlanSerializer,
    UserSubscriptionSerializer,
    ReadUserSubscriptionSerializer,
    FreezingRequestSerializer,
    SubscriptionAttendanceSerializer,
    WalkInTypeSerializer,
    ReadWalkInTypeSerializer,
    WalkInUserSerializer,
    ReadWalkInUserSerializer, ReadFreezingRequestsSerializer,
)


class PackagesViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = PackagesSerializer
    queryset = Package.objects.filter(is_safe_deleted=False).order_by("-created_at")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"is_active": ["exact"]}
    search_fields = [
        "id",
        "name",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadPackageSerializer
        return PackagesSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_safe_deleted=False).order_by("-created_at")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"package_id": ["exact"], "duration_type": ["exact"]}
    search_fields = [
        "id",
        "name",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadPlanSerializer
        return PlanSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = UserSubscriptionSerializer
    queryset = Subscription.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"plan_id": ["exact"], "user_id": ["exact"]}
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

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadUserSubscriptionSerializer
        return UserSubscriptionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FreezingRequestViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = FreezingRequestSerializer
    queryset = FreezingRequest.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "plan_id": ["exact"],
        "user_id": ["exact"],
        "requested_by_id": ["exact"],
    }
    search_fields = [
        "id",
        "user__first_name",
        "user__last_name",
        "user__mobile",
        "requested_by__first_name",
        "requested_by__last_name",
        "requested_by__mobile",
        "plan__name",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadFreezingRequestsSerializer
        return FreezingRequestSerializer


class SubscriptionAttendanceViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SubscriptionAttendanceSerializer
    queryset = SubscriptionAttendance.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"subscription_id": ["exact"], "user_id": ["exact"]}
    search_fields = [
        "id",
        "user__first_name",
        "user__last_name",
        "user__mobile",
    ]


class WalkInTypeViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = WalkInTypeSerializer
    queryset = WalkInType.objects.filter(is_safe_deleted=False)
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "id",
        "name",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadWalkInTypeSerializer
        return WalkInTypeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalkInUserViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = WalkInUserSerializer
    queryset = WalkInUser.objects.filter(is_safe_deleted=False)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"walk_in_type__id": ["exact"], "added_by__id": ["exact"]}
    search_fields = [
        "id",
        "full_name",
        "mobile",
        "added_by__first_name",
        "added_by__last_name",
        "added_by__mobile",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadWalkInUserSerializer
        return WalkInUserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
