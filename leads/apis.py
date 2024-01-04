from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from leads.models import Lead
from leads.serializers import LeadSerializer, ReadLeadSerializer


class LeadViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = LeadSerializer
    queryset = Lead.objects.filter(is_safe_deleted=False)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadLeadSerializer
        return LeadSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_safe_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
