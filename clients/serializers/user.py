from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.models import User
from clients.models.user import EmployeeAttendance
from clients.serializers import ReadGroupsSerializer
from clients.utility import generate_random_password, Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "gender",
            "groups",
            "avatar",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(generate_random_password())
        user.save()
        return user


class ReadUserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = PhoneNumberField()
    email = serializers.EmailField()
    gender = serializers.CharField()
    is_active = serializers.BooleanField()
    groups = ReadGroupsSerializer(many=True)


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = EmployeeAttendance
        fields = ["employee", "checkin_time", "checkout_time"]

    def validate_user(self, value):
        # Check if the requester is an admin
        if self.context["request"].user.is_superuser:
            # If admin, use the user from the request
            request_body_user = self.context["request"].data.get("employee")
            return User.objects.get(pk=request_body_user)
        else:
            # If not admin, use the default user
            return value
