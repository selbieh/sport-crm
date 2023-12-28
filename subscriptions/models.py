from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import TimeStampedModel, User
from subscriptions.utility import DURATION_TYPE_CHOICES, DAYS


# Create your models here.
class Package(TimeStampedModel):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")


class Plan(TimeStampedModel):
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="plans")
    name = models.CharField(max_length=150, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_type = models.CharField(
        max_length=50, choices=DURATION_TYPE_CHOICES, default=DAYS
    )
    number_of_days = models.IntegerField(null=False)
    number_of_sessions = models.IntegerField(null=True)
    number_of_duration_days = models.IntegerField(null=False)
    number_of_freezing_days = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.number_of_duration_days = self.number_of_days
        super(Plan, self).save(force_insert=False, force_update=False, using=None,
                                         update_fields=None)


class Subscription(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    freezing_days = models.IntegerField(default=False)

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")


class FreezingRequest(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_freezing_requests"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="plan_freezing_requests"
    )
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    duration = models.IntegerField(null=False)

    class Meta:
        verbose_name = _("Freezing Request")
        verbose_name_plural = _("Freezing Requests")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.duration = (self.end_date - self.start_date).days
        super(Plan, self).save(force_insert=False, force_update=False, using=None,
                                         update_fields=None)
