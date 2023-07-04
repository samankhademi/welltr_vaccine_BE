from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.models import BaseModel


# Create your models here.
class Exchange(BaseModel):
    name = models.CharField(_("exchange name"), max_length=50)
    state = models.CharField(_("exchange state, city"), max_length=50)
    address = models.CharField(_("exchange address"), max_length=100)
    users = models.ManyToManyField(
        "authentication.User",
        verbose_name=_("exchange users"),
        related_name="users",
        blank=True
    )
    phone = models.CharField(
        _("phone number"), max_length=30, blank=True, null=True
    )
