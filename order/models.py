from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.functions import code_generator
from utils.models import BaseModel


class VaccineCenter(BaseModel):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("vaccine center")
        verbose_name_plural = _("vaccine centers")


OPEN = "OPEN"
WAITING_FOR_DATA_SUBMISSION = "WAITING_FOR_DATA_SUBMISSION"
FULL_PAID = "FULL PAID"
PAID_20_PERCENT = "PAID 20 PERCENT"
WAITING_FOR_SETTING_FIRST_DOSE = "WAITING_FOR_SETTING_FIRST_DOSE"
WAITING_FOR_PAY = "WAITING_FOR_PAY"
WAITING_FOR_RECEIVING_FIRST_DOSE = "WAITING_FOR_RECEIVING_FIRST_DOSE"
WAITING_FOR_SETTING_SECOND_DOSE = "WAITING_FOR_SETTING_SECOND_DOSE"
WAITING_FOR_RECEIVING_SECOND_DOSE = "WAITING_FOR_RECEIVING_SECOND_DOSE"
DONE = "DONE"
ORDER_STATUS_CHOICES = [
    (OPEN, _("Open")),
    (WAITING_FOR_DATA_SUBMISSION, _("waiting for data submisson")),
    (FULL_PAID, _("full paid")),
    (PAID_20_PERCENT, _("paid 20 percent")),
    (WAITING_FOR_SETTING_FIRST_DOSE, _("Waiting for setting first dose")),
    (WAITING_FOR_PAY, _("Waiting for pay")),
    (WAITING_FOR_RECEIVING_FIRST_DOSE, _("Waiting for receiving first dose")),
    (WAITING_FOR_SETTING_SECOND_DOSE, _("Waiting for setting second dose")),
    (WAITING_FOR_RECEIVING_SECOND_DOSE, _("Waiting for receiving second dose")),
    (DONE, _("Done")),
]

FULL = "FULL"
PARTIAL = "PARTIAL"
EXCHANGE = "EXCHANGE"
USDT = "USDT"
PAYMENT_TYPE_CHOICES = [
    (FULL, _("FULL")),
    (PARTIAL, _("PARTIAL")),
    (EXCHANGE, _("EXCHANGE")),
    (USDT, _("USDT"))
]


class VaccineType(BaseModel):
    vaccine_type = models.CharField(
        _("vaccine type"), max_length=50, blank=True, null=True
    )
    is_available = models.BooleanField(_("is vaccine type available?"), default=True)

    def __str__(self):
        return self.vaccine_type

    class Meta:
        verbose_name = _("vaccine type")
        verbose_name_plural = _("vaccine types")


class Order(BaseModel):
    status = models.CharField(
        _("order status"), max_length=50, choices=ORDER_STATUS_CHOICES, default=OPEN
    )
    code = models.CharField(
        max_length=6, blank=True, editable=False, default=code_generator
    )
    vaccine_center = models.ForeignKey(
        "order.VaccineCenter",
        verbose_name=_("vaccine center"),
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("related user"),
        related_name="orders",
        on_delete=models.CASCADE,
    )
    vaccine_type = models.ForeignKey(
        VaccineType,
        verbose_name=_("vaccine type"),
        on_delete=models.SET_NULL,
        related_name="selected_orders",
        null=True,
        blank=True,
    )
    amount = models.FloatField(_("order amount in euro"), default=0)
    paid_amount = models.FloatField(_("order paid amount in euro"), default=0)
    payment_date = models.DateField(
        _("payment date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose1_flight_number = models.CharField(
        _("dose 1 flight number"), max_length=50, blank=True, null=True
    )
    dose1_transport_company_name = models.CharField(
        _("dose 1 transportation company name"), max_length=50, blank=True, null=True
    )
    dose1_arrival_date = models.DateField(
        _("dose 1 arrival date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose1_vaccine_center = models.ForeignKey(
        "order.VaccineCenter",
        verbose_name=_("dose1 vaccine center"),
        related_name="dose1_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    dose1_vaccine_type = models.ForeignKey(
        VaccineType,
        verbose_name=_("vaccine type"),
        on_delete=models.SET_NULL,
        related_name="dose1_orders",
        null=True,
        blank=True,
    )
    dose1_vaccination_date = models.DateField(
        _("dose1 vaccination date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose1_next_vaccination_date = models.DateField(
        _("dose1 next vaccination date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose2_flight_number = models.CharField(
        _("dose 1 flight number"), max_length=50, blank=True, null=True
    )
    dose2_transport_company_name = models.CharField(
        _("dose 1 transportation company name"), max_length=50, blank=True, null=True
    )
    dose2_arrival_date = models.DateField(
        _("dose 1 arrival date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose2_vaccine_center = models.ForeignKey(
        "order.VaccineCenter",
        verbose_name=_("dose2 vaccine center"),
        related_name="dose2_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    dose2_vaccine_type = models.ForeignKey(
        VaccineType,
        verbose_name=_("vaccine type"),
        on_delete=models.SET_NULL,
        related_name="dose2_orders",
        null=True,
        blank=True,
    )
    dose2_vaccination_date = models.DateField(
        _("dose2 vaccination date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dose2_next_vaccination_date = models.DateField(
        _("dose2 next vaccination date"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    payment_type = models.CharField(
        _("payment type"),
        max_length=50,
        choices=PAYMENT_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    hotel_package = models.ForeignKey(
        "order.HotelPackage",
        verbose_name=_("hotel package"),
        on_delete=models.SET_NULL,
        related_name="hotel_package_orders",
        null=True,
        blank=True,
    )
    is_used_coupon = models.BooleanField(_("is order used coupon ?"), default=False)
    wrong_coupon_count = models.IntegerField(_("wrong coupons counter"), default=0)
    usdt_token = models.CharField(
        _("usdt token"),
        max_length=400,
        null=True,
        blank=True,
    )
    usdt_address = models.CharField(
        _("usdt payment address"),
        max_length=100,
        null=True,
        blank=True,
    )
    usdt_payment_id = models.CharField(
        _("usdt payment ID"),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


AVAILABLE = "AVAILABLE"
USED = "USED"
DISABLED = "DISABLED"
COUPON_STATUS_CHOICES = [
    (AVAILABLE, _("AVAILABLE")),
    (USED, _("USED")),
    (DISABLED, _("DISABLED")),
]


class Coupon(BaseModel):
    pin = models.CharField(
        _("coupon pin"), max_length=50, blank=True, null=True
    )
    order = models.ForeignKey(
        "order.Order",
        verbose_name=_("related order"),
        on_delete=models.SET_NULL,
        related_name="coupons",
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("coupon status"), max_length=50, choices=COUPON_STATUS_CHOICES, default=AVAILABLE
    )
    off_percent = models.FloatField(
        _("coupon off percent"), default=15
    )

    def __str__(self):
        return self.pin

    class Meta:
        verbose_name = _("coupon")
        verbose_name_plural = _("coupon")


class HotelPackage(BaseModel):
    total_person = models.IntegerField(_("total person"), default=1)
    hotel_name = models.CharField(_("hotel name"), max_length=250)
    nights_num = models.IntegerField(_("number of nights"), default=1)
    price = models.FloatField(_("package price"), default=0)
    room_type_fa = models.TextField(_("room type in farsi"), blank=True, null=True)
    room_type_en = models.TextField(_("room type in english"), blank=True, null=True)
    room_type_tr = models.TextField(_("room type in turkish"), blank=True, null=True)
    desc_fa = models.TextField(_("farsi description"), blank=True, null=True)
    desc_en = models.TextField(_("english description"), blank=True, null=True)
    desc_tr = models.TextField(_("turkish description"), blank=True, null=True)
    address_fa = models.TextField(_("farsi address"), blank=True, null=True)
    address_en = models.TextField(_("english address"), blank=True, null=True)
    address_tr = models.TextField(_("turkish address"), blank=True, null=True)
    rank = models.FloatField(_("hotel star number"), default=0)
    image = models.ImageField(
        _("hotel image"), upload_to="hotels", blank=True, null=True
    )


IRR = "IRR"
USDT_C = "USDT"

CURRENCY_CHOICES = [
    (IRR, _("Iranian rial")),
    (USDT_C, _("usdt"))
]


class CurrencyExchangeRate(BaseModel):
    currency_name = models.CharField(
        _("currency ISO code"),
        max_length=5,
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
    )
    exchange_rate = models.FloatField(_("exchange by currency name"), default=1)

