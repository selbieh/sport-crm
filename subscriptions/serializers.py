from datetime import timedelta

from rest_framework import serializers

from Academy_class.models import ClassAttendance
from Academy_class.serializers import ReadAcademyClassSerializer
from clients.models import User
from clients.serializers import ReadUserDataSerializer, ReadGroupsSerializer
from subscriptions.models import (
    Package,
    Plan,
    Subscription,
    FreezingRequest,
    SubscriptionAttendance,
    WalkInType,
    WalkInUser,
)
from subscriptions.utility import DAYS


class PackagesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Package
        exclude = ("is_safe_deleted",)


class ReadPackageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class PlanSerializer(serializers.ModelSerializer):
    package = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), required=True
    )

    class Meta:
        model = Plan
        exclude = ("is_safe_deleted", "number_of_duration_days")

    def validate(self, attrs):
        if attrs["duration_type"] == DAYS:
            if "number_of_sessions" in attrs:
                raise serializers.ValidationError(
                    "type days not have number of sessions"
                )
        return attrs


class ReadPlanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    package = ReadPackageSerializer()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=3)
    duration_type = serializers.CharField()
    number_of_days = serializers.IntegerField()
    number_of_sessions = serializers.IntegerField()
    number_of_duration_days = serializers.IntegerField()
    number_of_freezing_days = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class UserSubscriptionSerializer(serializers.ModelSerializer):
    added_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Subscription
        exclude = ("end_date", "is_safe_deleted", "freezing_days")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.end_date = instance.start_date + timedelta(
            days=instance.plan.number_of_duration_days
        )
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.end_date = instance.start_date + timedelta(
            days=instance.plan.number_of_duration_days
        )
        instance.save()
        return instance


class ReadUserSubscriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    plan = ReadPlanSerializer()
    user = ReadUserDataSerializer()
    added_by = ReadUserDataSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    freezing_days = serializers.IntegerField()
    payment_method = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    discount_type = serializers.CharField()
    discount = serializers.FloatField()
    price_after_discount = serializers.DecimalField(max_digits=10, decimal_places=3)
    refunded_amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    sales_person = ReadUserDataSerializer()
    comments = serializers.CharField()
    created_at = serializers.DateTimeField()


class FreezingRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    requested_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = FreezingRequest
        exclude = ["is_safe_deleted", "duration"]

    def validate(self, attrs):
        plan = attrs["plan"]
        if not plan.number_of_freezing_days:
            raise serializers.ValidationError("Plan is not freezable")
        return attrs

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

    def create(self, validated_data):
        try:
            freezing_request = super().create(validated_data)
            user_subscription = Subscription.objects.get(
                user=freezing_request.user, plan=freezing_request.plan
            )
            user_subscription.end_date += timedelta(days=freezing_request.duration)
            user_subscription.freezing_days += freezing_request.duration
            user_subscription.save()
            return freezing_request
        except Subscription.DoesNotExist:
            raise serializers.ValidationError(
                "User not have subscription to add freezing requests."
            )


class ReadFreezingRequestsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = ReadUserDataSerializer()
    plan = ReadPlanSerializer()
    requested_by = ReadUserDataSerializer()
    duration = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    created_at = serializers.DateTimeField()


class SubscriptionAttendanceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = SubscriptionAttendance
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


class WalkInTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkInType
        exclude = ("is_safe_deleted",)


class ReadWalkInTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=3)
    created_at = serializers.DateTimeField()


class WalkInUserSerializer(serializers.ModelSerializer):
    walk_in_type = serializers.PrimaryKeyRelatedField(
        queryset=WalkInType.objects.all(), required=True
    )
    added_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = WalkInUser
        exclude = ("is_safe_deleted",)

    def create(self, validated_data):
        walk_in_user = super().create(validated_data)
        academy_class = validated_data.get("academy_class")
        if academy_class:
            ClassAttendance.objects.create(
                academy_class=academy_class, walk_in_user=walk_in_user
            )

        return validated_data


class ReadWalkInUserSerializer(serializers.ModelSerializer):
    walk_in_type = ReadWalkInTypeSerializer()
    added_by = ReadUserDataSerializer()

    class Meta:
        model = WalkInUser
        exclude = ("is_safe_deleted",)


class UserProfileSubscriptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    plan = ReadPlanSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    freezing_days = serializers.IntegerField()


class ReadUserClassProfile(serializers.Serializer):
    id = serializers.IntegerField()
    academy_class = ReadAcademyClassSerializer()
    subscription = UserProfileSubscriptionsSerializer()
    created_at = serializers.DateTimeField()


class UserProfileSerializer(ReadUserDataSerializer):
    avatar = serializers.ImageField()
    groups = ReadGroupsSerializer(many=True)
    subscriptions = UserProfileSubscriptionsSerializer(many=True)
    user_class_attendances = ReadUserClassProfile(many=True, allow_null=True)
