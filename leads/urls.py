from django.urls import path, include
from rest_framework.routers import DefaultRouter

from leads.apis import LeadViewSet

router = DefaultRouter()
router.register(r"lead", LeadViewSet, basename="leads_api")

urlpatterns = [path("", include(router.urls))]
