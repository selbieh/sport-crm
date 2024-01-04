from rest_framework import status
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
)


class PackagesViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = PackagesSerializer
    queryset = Package.objects.filter(is_safe_deleted=False).order_by("-created_at")

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


class SubscriptionAttendanceViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SubscriptionAttendanceSerializer
    queryset = SubscriptionAttendance.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )


class WalkInTypeViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = WalkInTypeSerializer
    queryset = WalkInType.objects.filter(is_safe_deleted=False)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
