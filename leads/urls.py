from django.urls import path, include
from rest_framework.routers import DefaultRouter

from leads.apis import LeadViewSet, ConvertToMemberApi

router = DefaultRouter()
router.register(r"lead", LeadViewSet, basename="leads_api")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "convert-member/<lead_id>/",
        ConvertToMemberApi.as_view(),
        name="convert_lead_to_member_api",
    ),
]
