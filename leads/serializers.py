from django.shortcuts import get_object_or_404
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.serializers import ReadUserDataSerializer, UserSerializer
from leads.models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        exclude = ("is_safe_deleted", "user")


class ReadLeadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = PhoneNumberField()
    email = serializers.EmailField()
    gender = serializers.CharField()
    assigned_to = ReadUserDataSerializer()
    status = serializers.CharField()
    notes = serializers.CharField()
    address = serializers.CharField()
    occupation = serializers.CharField()
    organization = serializers.CharField()
    website = serializers.URLField()
    source = serializers.CharField()
    created_at = serializers.DateTimeField()


class ConvertLeadToMemberSerializer(UserSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        lead = get_object_or_404(Lead, pk=self.context.get('lead_id'))
        lead.user = user
        lead.save()
        return user