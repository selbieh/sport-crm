from rest_framework import serializers

from clients.models import User
from clients.serializers import ReadUserDataSerializer
from Academy_class.models import AcademyClass, ClassSubscription, ClassAttendance


class AcademyClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyClass
        exclude = ("is_safe_deleted",)


class ReadAcademyClassSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    dates = serializers.CharField()
    time_from = serializers.TimeField()
    time_to = serializers.TimeField()
    instructor = ReadUserDataSerializer()
    maximum_capacity = serializers.IntegerField()
    gender = serializers.CharField()
    age_group = serializers.IntegerField()
    location = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ClassSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = ClassSubscription
        exclude = ("is_safe_deleted",)

    def validate_user(self, value):
        # Check if the requester is an admin
        if self.context["request"].user.is_superuser:
            # If admin, use the user from the request
            request_body_user = self.context["request"].data.get("user")
            return User.objects.get(pk=request_body_user)
        else:
            # If not admin, use the default user
            return value


class ReadUserSportSubscriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    academy_class = ReadAcademyClassSerializer()
    user = ReadUserDataSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class ClassAttendanceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = ClassAttendance
        exclude = [
            "is_safe_deleted",
        ]

    def validate_user(self, value):
        # Check if the requester is an admin
        if self.context["request"].user.is_superuser:
            # If admin, use the user from the request
            request_body_user = self.context["request"].data.get("user")
            return User.objects.get(pk=request_body_user)
        else:
            # If not admin, use the default user
            return value
