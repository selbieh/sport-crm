"""
URL configuration for gym_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from clients.apis.auth import MyTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="GYM CRM API",
        default_version="v1",
        description="Apis description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", MyTokenObtainPairView.as_view(), name="login"),
    path("api/v1/client/", include("clients.urls"), name="client-v1"),
    path("api/v1/subscription/", include("subscriptions.urls"), name="subscription-v1"),
    path("api/v1/class/", include("Academy_class.urls"), name="class-v1"),
    path("api/v1/", include("leads.urls"), name="lead-v1"),
    path("api/v1/task/", include("tasks.urls"), name="tasks-v1"),
    path("api/dashboard/v1/", include("dashboard.urls"), name="dashboard-v1"),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
