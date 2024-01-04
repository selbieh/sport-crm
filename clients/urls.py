from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients.apis import (
    RolesViewSet,
    ListPermissionsApi,
    UserViewSet,
    ChangePasswordApi,
)

router = DefaultRouter()
router.register(r"role", RolesViewSet, basename="roles_api")
router.register(r"user", UserViewSet, basename="users_api")

urlpatterns = [
    path("", include(router.urls)),
    path("permissions/", ListPermissionsApi.as_view(), name="permissions"),
    path(
        "change-password/<int:pk>/", ChangePasswordApi.as_view(), name="change_password"
    ),
]
