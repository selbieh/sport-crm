from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients.apis import (
    RolesViewSet,
    ListPermissionsApi,
    UserViewSet,
    ChangePasswordApi,
    EmployeeAttendanceViewSet,
    MemberProfileApi, GetMemberProfileByIdApi,
)

router = DefaultRouter()
router.register(r"role", RolesViewSet, basename="roles_api")
router.register(r"user", UserViewSet, basename="users_api")
router.register(
    r"employee/attendance",
    EmployeeAttendanceViewSet,
    basename="employee_attendance_api",
)

urlpatterns = [
    path("", include(router.urls)),
    path("permissions/", ListPermissionsApi.as_view(), name="permissions"),
    path(
        "change-password/<int:pk>/", ChangePasswordApi.as_view(), name="change_password"
    ),
    path("member/profile/", MemberProfileApi.as_view(), name="member_profile_api"),
    path("member/<int:pk>/", GetMemberProfileByIdApi.as_view(), name="get_member_profile_by_id_api")
]
