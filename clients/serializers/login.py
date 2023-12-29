from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from clients.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["user_id"] = str(user.id)
        return token

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        data = {}
        try:
            user = User.objects.get(mobile=mobile)
            if not user.is_whatsapp_verified:
                raise serializers.ValidationError("user is not verified")
            data = super(MyTokenObtainPairSerializer, self).validate(attrs)
            data["groups"] = user.groups.values_list("name", flat=True)
            data["admin"] = user.is_superuser
        except User.DoesNotExist:
            data.update({"error": "user does not exist"})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=128, write_only=True, required=True, min_length=8
    )
    confirm_password = serializers.CharField(
        max_length=128, write_only=True, required=True, min_length=8
    )

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": _("password must match")})
        return data

    def update(self, instance, validated_data):
        password = validated_data["new_password"]
        instance.set_password(password)
        instance.save()
        return instance
