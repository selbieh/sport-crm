from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import TimeStampedModel, User
from tasks.utility import NEW, STATUS_CHOICES, PRIORITY_CHOICES


# Create your models here.
class Task(TimeStampedModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_by_tasks", null=True
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="assigned_to_tasks",
        null=True,
    )
    deadline = models.DateField(null=False)
    reminder_intervals = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(
        max_length=50, null=False, choices=STATUS_CHOICES, default=NEW
    )
    priority = models.CharField(
        max_length=50, null=True, blank=True, choices=PRIORITY_CHOICES
    )
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
