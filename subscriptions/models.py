from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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
    price = models.DecimalField(max_digits=10, decimal_places=3)
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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.number_of_duration_days = self.number_of_days
        super(Plan, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )


class Subscription(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    added_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="added_by_subscriptions", null=True
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    freezing_days = models.IntegerField(default=False)
    payment_method = models.CharField(
        _("payment_method"), max_length=255, null=True, blank=True
    )
    total_amount = models.DecimalField(
        _("total_amount"), max_digits=10, decimal_places=3, null=True
    )
    discount_type = models.CharField(
        _("discount_type"), max_length=150, null=True, blank=True
    )
    discount = models.FloatField(_("discount"), null=True, blank=True)
    price_after_discount = models.DecimalField(
        _("price_after_discount"), max_digits=10, decimal_places=3, null=True
    )
    sales_person = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sales_person_subscriptions",
        null=True,
    )
    comments = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.discount_type:
            self.total_amount = self.plan.price
            self.price_after_discount = self.plan.price
        super(Subscription, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )


class FreezingRequest(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_freezing_requests", null=True
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, related_name="plan_freezing_requests", null=True
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="requested_by_freezing_requests",
        null=True,
    )
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    duration = models.IntegerField(null=False)

    class Meta:
        verbose_name = _("Freezing Request")
        verbose_name_plural = _("Freezing Requests")

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days
        super(FreezingRequest, self).save(*args, **kwargs)


class SubscriptionAttendance(TimeStampedModel):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.PROTECT, related_name="subscription_attendances"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_attendances"
    )
    checkin_time = models.TimeField(null=True)
    checkout_time = models.TimeField(null=True)

    class Meta:
        verbose_name = _("Subscription Attendance")
        verbose_name_plural = _("Subscription Attendance")


class WalkInType(TimeStampedModel):
    name = models.CharField(_("name"), max_length=155, null=False, blank=False)
    description = models.TextField(_("description"), null=True, blank=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=3)

    class Meta:
        verbose_name = _("WalkIn Type")
        verbose_name_plural = _("WalkIn Types")


class WalkInUser(TimeStampedModel):
    walk_in_type = models.ForeignKey(
        WalkInType, on_delete=models.PROTECT, related_name="walk_in_users"
    )
    full_name = models.CharField(
        _("full_name"), max_length=255, null=False, blank=False
    )
    mobile = PhoneNumberField(_("mobile"), null=False, blank=False)
    added_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="added_by_walk_in_users", null=True
    )
    payment_method = models.CharField(
        _("payment_method"), max_length=255, null=True, blank=True
    )
    total_amount = models.DecimalField(
        _("total_amount"), max_digits=10, decimal_places=3
    )
    discount_type = models.CharField(
        _("discount_type"), max_length=150, null=True, blank=True
    )
    discount = models.FloatField(_("discount"), null=True, blank=True)
    price_after_discount = models.DecimalField(
        _("price_after_discount"), max_digits=10, decimal_places=3
    )
    notes = models.TextField(_("notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("WalkIn User")
        verbose_name_plural = _("WalkIn Users")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.discount_type:
            self.total_amount = self.walk_in_type.price
            self.price_after_discount = self.walk_in_type.price
        super(WalkInUser, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
