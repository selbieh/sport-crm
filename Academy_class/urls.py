from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Academy_class.apis import (
    AcademyClassViewSet,
    ClassSubscriptionViewSet,
    ClassAttendanceViewSet,
)

router = DefaultRouter()
router.register(r"academy-class", AcademyClassViewSet, basename="academy_class_api")
router.register(
    r"subscription-class", ClassSubscriptionViewSet, basename="subscription_class_api"
)
router.register(
    r"class-attendance", ClassAttendanceViewSet, basename="class_attendance_api"
)

urlpatterns = [
    path("", include(router.urls)),
]
