from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from clients.models import TimeStampedModel, User
from clients.utility import GENDER_CHOICES
from leads.utility import STATUS_CHOICES, NEW, SOURCE_CHOICES


# Create your models here.
class Lead(TimeStampedModel):
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    mobile = PhoneNumberField(_("mobile"), null=False, blank=False, unique=True)
    email = models.EmailField(_("email"), max_length=150, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=50, default=GENDER_CHOICES)
    assigned_to = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="assigned_to_leads"
    )
    status = models.CharField(
        _("status"), max_length=50, choices=STATUS_CHOICES, default=NEW
    )
    notes = models.TextField(_("notes"), null=True)
    address = models.CharField(_("address"), max_length=255, null=True, blank=True)
    occupation = models.CharField(
        _("occupation"), max_length=255, null=True, blank=True
    )
    organization = models.TextField(_("organization"), null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True)
    source = models.CharField(
        _("lead_source"), max_length=150, choices=SOURCE_CHOICES, null=True, blank=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_lead"
    )

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")
