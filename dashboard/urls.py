from django.urls import path, include

from dashboard.apis import (
    HomeDashboardExpirationApi,
    HomeDashboardAnalyticsApi,
    HomeMemberShipSalesSubscriptionApi,
    HomeMemberShipSalesClassApi,
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
        "memberships/subscription/analytics/",
        HomeMemberShipSalesSubscriptionApi.as_view(),
        name="home-membership-subscription-analytics",
    ),
    path(
        "memberships/classes/analytics/",
        HomeMemberShipSalesClassApi.as_view(),
        name="home-membership-sales-analytics",
    ),
]
