from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import TimeStampedModel, User
from clients.utility import GENDER_CHOICES
from Academy_class.utility import MALE
from subscriptions.models import Subscription, WalkInUser


# Create your models here.
class AcademyClass(TimeStampedModel):
    name = models.CharField(max_length=150, null=False, blank=False)
    dates = models.JSONField(default=list, null=True, blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)
    instructor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="instructor_sport_classes"
    )
    maximum_capacity = models.IntegerField(default=0)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=MALE)
    age_group = models.CharField(max_length=155, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Academy Class")
        verbose_name_plural = _("Academy Classes")


# class ClassSubscription(TimeStampedModel):
#     user = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name="user_class_subscriptions"
#     )
#     academy_class = models.ForeignKey(
#         AcademyClass,
#         on_delete=models.PROTECT,
#         related_name="academy_class_subscriptions",
#         null=True,
#     )
#     start_date = models.DateField(auto_now_add=True)
#     end_date = models.DateField(null=True)
#
#     class Meta:
#         verbose_name = _("Class Subscription")
#         verbose_name_plural = _("Class Subscriptions")


class ClassAttendance(TimeStampedModel):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="class_subscription_attendances",
        null=True,
    )
    academy_class = models.ForeignKey(
        AcademyClass,
        on_delete=models.PROTECT,
        related_name="academy_class_attendance",
        null=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_class_attendances", null=True
    )
    walk_in_user = models.ForeignKey(
        WalkInUser,
        on_delete=models.PROTECT,
        related_name="walk_in_user_class_attendance",
        null=True,
    )
    checkin_time = models.TimeField(null=True)
    checkout_time = models.TimeField(null=True)

    class Meta:
        verbose_name = _("Class Attendance")
        verbose_name_plural = _("Class Attendance")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.subscription:
            self.subscription.plan.number_of_sessions -= 1
            self.subscription.plan.save()
        super(ClassAttendance, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
