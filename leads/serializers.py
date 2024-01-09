from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.models import User
from clients.serializers import ReadUserDataSerializer, UserSerializer
from clients.utility import generate_random_password
from leads.models import Lead
from subscriptions.models import Subscription
from subscriptions.serializers import UserSubscriptionSerializer


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


class ConvertLeadToMemberSerializer(UserSubscriptionSerializer):
    class Meta:
        model = Subscription
        exclude = ("user", "end_date", "is_safe_deleted", "freezing_days")

    def create_lead_user(self):
        lead = get_object_or_404(Lead, pk=self.context.get("lead_id"))
        lead_user = User.objects.create(
            username=lead.email,
            email=lead.email,
            first_name=lead.first_name,
            last_name=lead.last_name,
            mobile=lead.mobile,
            gender=lead.gender,
            referred_by=lead.assigned_to
        )
        lead_user.set_password(generate_random_password())
        lead_user.save()
        lead.user = lead_user
        lead.save()
        return lead_user

    def create(self, validated_data):
        with transaction.atomic():
            lead_user = self.create_lead_user()
            instance = Subscription.objects.create(user=lead_user, **validated_data)
            instance.end_date = instance.start_date + timedelta(
                days=instance.plan.number_of_duration_days
            )
            instance.save()
        return instance
