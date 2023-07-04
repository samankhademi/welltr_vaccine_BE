from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.models import BaseModel


IN_PROGRESS = "IN_PROGRESS"
UNKNOWN = "UNKNOWN"
FAILED = "FAILED"
SUCCESS = "SUCCESS"
PAYMENT_STATUS_CHOICES = [
    (IN_PROGRESS, _("CREATED")),
    (FAILED, _("FAILED")),
    (UNKNOWN, _("UNKNOWN")),
    (SUCCESS, _("SUCCESS"))
]


class PaymentTransaction(BaseModel):
    status = models.CharField(
        _("payment status"), max_length=50, choices=PAYMENT_STATUS_CHOICES, default=IN_PROGRESS
    )
    transaction_id = models.CharField(
        _("transaction id"), max_length=100, blank=True, null=True
    )
    order = models.ForeignKey(
        "order.Order",
        verbose_name=_("related order"),
        on_delete=models.SET_NULL,
        related_name="payments",
        blank=True,
        null=True,
    )
    transaction_response = models.TextField(
        _("transaction response log"), max_length=1500, blank=True, null=True
    )
    transaction_request = models.TextField(
        _("transaction request log"), max_length=1500, blank=True, null=True
    )
    exchange = models.ForeignKey(
        "exchange.Exchange",
        verbose_name=_("related exchange"),
        on_delete=models.SET_NULL,
        related_name="transaction_exchange",
        blank=True,
        null=True,
        default=None
    )
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("exchange user"),
        on_delete=models.SET_NULL,
        related_name="transaction_user",
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        verbose_name = _("payment transaction")
        verbose_name_plural = _("payment transactions")
