from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import TimeStampedModel, User


# Create your models here.
class Notification(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notifications"
    )
    title = models.CharField(max_length=150, null=False, blank=False)
    message = models.TextField()
    source = models.JSONField(default=dict, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
