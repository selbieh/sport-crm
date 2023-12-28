from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients.apis import RolesViewSet, ListPermissionsApi
from clients.apis.user import UserViewSet

router = DefaultRouter()
router.register(r"role", RolesViewSet, basename="roles_api")
router.register(r"user", UserViewSet, basename="roles_api")

urlpatterns = [
    path("", include(router.urls)),
    path("permissions/", ListPermissionsApi.as_view(), name="permissions"),
]
