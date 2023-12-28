from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from clients.models import TimeStampedModel
from clients.utility import upload_avatar, GENDER_CHOICES, ROLE_CHOICES, CUSTOMER


class User(AbstractUser, TimeStampedModel):
    username = models.CharField(_("username"), max_length=150, null=True, blank=True)
    email = models.EmailField(_("email"), max_length=150, null=True, blank=True)
    mobile = PhoneNumberField(_("mobile"), blank=False, null=False, unique=True)
    whatsapp_number = PhoneNumberField(
        _("whatsapp_number"), null=True, blank=True, unique=True
    )
    gender = models.CharField(_("gender"), max_length=50, default=GENDER_CHOICES)
    is_whatsapp_verified = models.BooleanField(_("is_mobile_verified"), default=False)
    avatar = models.FileField(upload_to=upload_avatar, blank=True, null=True)

    EMAIL_FIELD = "mobile"
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return str(self.mobile)

    # def save(self, *args, **kwargs):
    #     group, created = Group.objects.get_or_create(name=self.role)
    #     super().save(*args, **kwargs)
    #     self.groups.add(group.id)
