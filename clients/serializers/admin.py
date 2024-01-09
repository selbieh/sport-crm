from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def create(self, validated_data):
        group_name = validated_data["name"]
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            permissions = validated_data.get("permissions", None)
            if permissions:
                group.permissions.add(*permissions)
        return group


class ReadPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()


class ReadGroupsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    permissions = ReadPermissionSerializer(many=True)
