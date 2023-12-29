from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import TimeStampedModel, User
from clients.utility import GENDER_CHOICES
from sport_classes.utility import MALE


# Create your models here.
class SportClass(TimeStampedModel):
    name = models.CharField(max_length=150, null=False, blank=False)
    dates = models.CharField(max_length=255, null=True, blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)
    instructor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="instructor_sport_classes"
    )
    maximum_capacity = models.IntegerField(default=0)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=MALE)
    age_group = models.IntegerField(default=0)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Sport Class")
        verbose_name_plural = _("Sport Classes")


class ClassSubscription(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_class_subscriptions"
    )
    sport_class = models.ForeignKey(
        SportClass, on_delete=models.PROTECT, related_name="sport_class_subscriptions"
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("Class Subscription")
        verbose_name_plural = _("Class Subscriptions")


class ClassAttendance(TimeStampedModel):
    subscription = models.ForeignKey(
        ClassSubscription,
        on_delete=models.PROTECT,
        related_name="class_subscription_attendances",
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_class_attendances"
    )
    is_attended = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Class Attendance")
        verbose_name_plural = _("Class Attendance")
