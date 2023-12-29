from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sport_classes.apis import (
    SportClassViewSet,
    ClassSubscriptionViewSet,
    ClassAttendanceViewSet,
)

router = DefaultRouter()
router.register(r"sport-class", SportClassViewSet, basename="sport_class_api")
router.register(
    r"subscription-class", ClassSubscriptionViewSet, basename="subscription_class_api"
)
router.register(
    r"class-attendance", ClassAttendanceViewSet, basename="class_attendance_api"
)

urlpatterns = [
    path("", include(router.urls)),
]
