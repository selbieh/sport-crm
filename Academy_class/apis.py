from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Academy_class.models import AcademyClass, ClassSubscription, ClassAttendance
from Academy_class.serializers import (
    AcademyClassSerializer,
    ReadAcademyClassSerializer,
    ClassSubscriptionSerializer,
    ReadUserSportSubscriptionSerializer,
    ClassAttendanceSerializer,
)


class AcademyClassViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = AcademyClassSerializer
    queryset = AcademyClass.objects.filter(is_safe_deleted=False).order_by(
        "-created_at"
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "instructor_id": ["exact"],
        "gender": ["exact"],
        "is_active": ["exact"],
        "age_group": ["exact"],
        "maximum_capacity": ["exact"],
    }
    search_fields = [
        "id",
        "name",
        "instructor__first_name",
        "instructor__last_name",
        "instructor__mobile",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadAcademyClassSerializer
        return AcademyClassSerializer

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"user_id": ["exact"], "academy_class_id": ["exact"]}
    search_fields = ["id", "user__first_name", "user__last_name", "user__mobile"]

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
