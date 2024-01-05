from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.apis import TaskViewSet

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="tasks_api")

urlpatterns = [
    path("", include(router.urls)),
]
