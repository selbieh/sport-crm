from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sport_classes.models import SportClass, ClassSubscription, ClassAttendance
from sport_classes.serializers import (
    SportClassSerializer,
    ReadSportClassSerializer,
    ClassSubscriptionSerializer,
    ReadUserSportSubscriptionSerializer,
    ClassAttendanceSerializer,
)


class SportClassViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SportClassSerializer
    queryset = SportClass.objects.filter(is_safe_deleted=False).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadSportClassSerializer
        return SportClassSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClassSubscriptionViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ClassSubscriptionSerializer
    queryset = ClassSubscription.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassSubscriptionSerializer
        return ReadUserSportSubscriptionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClassAttendanceViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ClassAttendanceSerializer
    queryset = ClassAttendance.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
