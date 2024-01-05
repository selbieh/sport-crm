from django.urls import path, include
from rest_framework.routers import DefaultRouter

from subscriptions.apis import (
    PackagesViewSet,
    PlanViewSet,
    UserSubscriptionViewSet,
    FreezingRequestViewSet,
    SubscriptionAttendanceViewSet,
    WalkInTypeViewSet,
    WalkInUserViewSet,
)

router = DefaultRouter()
router.register(r"packages", PackagesViewSet, basename="packages_api")
router.register(r"plans", PlanViewSet, basename="plans_api")
router.register(r"user", UserSubscriptionViewSet, basename="subscriptions_api")
router.register(
    r"freezing-request", FreezingRequestViewSet, basename="freezing_requests_api"
)
router.register(r"attendance", SubscriptionAttendanceViewSet, basename="attendance_api")
router.register(r"walk-in-type", WalkInTypeViewSet, basename="walk-in-type_api")
router.register(r"walk-in-user", WalkInUserViewSet, basename="walk-in-user_api")

urlpatterns = [
    path("", include(router.urls)),
]
