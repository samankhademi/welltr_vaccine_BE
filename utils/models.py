import uuid

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords


class BaseModelQuerySet(QuerySet):
    def delete(self):
        return super(BaseModelQuerySet, self).update(
            is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super(BaseModelQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None, is_deleted=False)


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseModelQuerySet(self.model).filter(is_deleted=False)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def delete(self):
        return self.get_queryset().delete()


class BaseModel(models.Model):
    history = HistoricalRecords(inherit=True)
    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4, unique=True, editable=False)

    created_at = models.DateTimeField(
        _("created at"), editable=False, auto_now_add=True, null=True
    )

    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        editable=False,
    )

    deleted_at = models.DateTimeField(
        _("updated at"),
        blank=True,
        null=True
    )

    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
