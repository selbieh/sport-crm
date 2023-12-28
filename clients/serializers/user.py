from rest_framework import serializers

from clients.models import User
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
