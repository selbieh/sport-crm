from rest_framework import serializers

from clients.models import User
from clients.serializers import ReadUserDataSerializer
from subscriptions.serializers import ReadPlanSerializer


class HomeDashboardExpirationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    plan = ReadPlanSerializer()
    user = ReadUserDataSerializer()
    added_by = ReadUserDataSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    sales_person = ReadUserDataSerializer()


class UserSubscriptionSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    subscriptions_count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3)

    def get_user(self, obj):
        user = User.objects.get(id=obj["user"])
        return ReadUserDataSerializer(user).data
