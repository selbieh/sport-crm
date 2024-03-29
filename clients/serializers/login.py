from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from clients.models import User
from clients.serializers import ReadGroupsSerializer


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
        user = get_object_or_404(User, mobile=mobile, is_safe_deleted=False)
        if not user.is_whatsapp_verified:
            raise serializers.ValidationError("user is not verified")
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data["groups"] = ReadGroupsSerializer(user.groups.all(), many=True).data
        data["admin"] = user.is_superuser
        data["user_id"] = user.id
        data["name"] = user.get_full_name()
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
