from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed "created at" and
    "modified at" fields.
    """

    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified_at"), auto_now_add=True)
    is_safe_deleted = models.BooleanField(_("is_safe_delete"), default=False)

    class Meta:
        abstract = True
