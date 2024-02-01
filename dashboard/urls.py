from django.urls import path, include

from dashboard.apis import (
    HomeDashboardExpirationApi,
    HomeDashboardAnalyticsApi,
    HomeMemberShipSalesClassesApi,
)

urlpatterns = [
    path(
        "expire-subscriptions/",
        HomeDashboardExpirationApi.as_view(),
        name="home-dashboard-expiration-subscriptions",
    ),
    path(
        "analytics/",
        HomeDashboardAnalyticsApi.as_view(),
        name="home-dashboard-analytics",
    ),
    path(
        "memberships/analytics/",
        HomeMemberShipSalesClassesApi.as_view(),
        name="home-membership-analytics",
    ),
]
