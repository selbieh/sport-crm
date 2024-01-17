from rest_framework import serializers

from clients.models import User
from clients.serializers import ReadUserDataSerializer
from Academy_class.models import AcademyClass, ClassAttendance


class AcademyClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyClass
        exclude = ("is_safe_deleted",)


class ReadAcademyClassSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    dates = serializers.ListField()
    time_from = serializers.TimeField()
    time_to = serializers.TimeField()
    instructor = ReadUserDataSerializer()
    maximum_capacity = serializers.IntegerField()
    gender = serializers.CharField()
    age_group = serializers.CharField()
    location = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


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
        if self.context["request"].user.is_superuser:
            # If admin, use the user from the request data
            request_body_user = self.initial_data.get("user")
            if request_body_user is not None:
                try:
                    return User.objects.get(pk=request_body_user)
                except User.DoesNotExist:
                    raise serializers.ValidationError("User not found.")
            else:
                raise serializers.ValidationError("User field is required for admin.")
        else:
            # If not admin, use the default user
            return value
