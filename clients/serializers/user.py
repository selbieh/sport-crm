from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.models import User
from clients.models.user import EmployeeAttendance
from clients.serializers import ReadGroupsSerializer
from clients.utility import generate_random_password, Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    avatar = Base64ImageField(required=False)
    password = serializers.CharField(min_length=5, write_only=True)
    confirm_password = serializers.CharField(min_length=5, write_only=True)

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
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs.get("confirm_password") != attrs.get("password"):
            raise serializers.ValidationError("passwords does not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = super().create(validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ReadUserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = PhoneNumberField()
    email = serializers.EmailField()
    gender = serializers.CharField()
    is_active = serializers.BooleanField()


class ReadUserSerializer(ReadUserDataSerializer):
    avatar = serializers.ImageField()
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
