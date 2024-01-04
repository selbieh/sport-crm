from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from clients.models import User
from clients.serializers import ReadGroupsSerializer
from clients.utility import generate_random_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "mobile", "email", "gender", "groups"]

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
    groups = ReadGroupsSerializer(many=True)
