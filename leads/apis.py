from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from clients.models import User
from leads.models import Lead
from leads.serializers import (
    LeadSerializer,
    ReadLeadSerializer,
    ConvertLeadToMemberSerializer,
)


class LeadViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = LeadSerializer
    queryset = Lead.objects.filter(is_safe_deleted=False)
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "mobile"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadLeadSerializer
        return LeadSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConvertToMemberApi(CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ConvertLeadToMemberSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"lead_id": self.kwargs.get("lead_id")})
        return context
