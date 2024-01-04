from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.serializers import ReadUserDataSerializer
from leads.models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        exclude = ("is_safe_deleted",)


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
