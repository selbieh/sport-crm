from django.urls import path, include
from rest_framework.routers import DefaultRouter

from subscriptions.apis import PackagesViewSet, PlanViewSet, UserSubscriptionViewSet, FreezingRequestViewSet

router = DefaultRouter()
router.register(r"packages", PackagesViewSet, basename="packages_api")
router.register(r"plans", PlanViewSet, basename="plans_api")
router.register(r"subscription", UserSubscriptionViewSet, basename="subscriptions_api")
router.register(r"freezing-request", FreezingRequestViewSet, basename="freezing_requests_api")
urlpatterns = [
    path("", include(router.urls)),
]
