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


class SalesSubscriptionSerializer(serializers.Serializer):
    sales_person = serializers.SerializerMethodField()
    subscriptions_count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3)

    def get_sales_person(self, obj):
        user_id = obj["sales_person"]
        if user_id:
            user = User.objects.get(id=user_id)
            return ReadUserDataSerializer(user).data
        return None


class SalesClassSerializer(serializers.Serializer):
    instructor = serializers.SerializerMethodField()
    classes_count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3)

    def get_instructor(self, obj):
        user = User.objects.get(id=obj["instructor"])
        return ReadUserDataSerializer(user).data
