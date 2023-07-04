import datetime
import json
import random

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ip2geotools.databases.noncommercial import DbIpCity

from authentication.models import User, OTP
from exchange.models import Exchange
from order.models import Order, PARTIAL, EXCHANGE, WAITING_FOR_RECEIVING_FIRST_DOSE, \
    WAITING_FOR_PAY, USDT
from order.service import exchange_usdt_to_euro, exchange_euro_to_usdt
from utils.functions import get_client_ip

from .models import PaymentTransaction, FAILED, SUCCESS, UNKNOWN
from django.db import transaction


def transaction_inquiry(transaction_id: str):
    import requests

    url = "{}/exts/payment/0/v1/999/1".format(settings.SUPER_PAY_URL)

    user_transaction = PaymentTransaction.objects.get(uuid=transaction_id)

    inquiry_data = {
        "hi": 1919,
        "htran": random.randint(0, 999999999999),
        "htime": int(user_transaction.created_at.timestamp()),
        "hkey": "40efc1c1-f7f3-44bf-bdb5-fb54bf285648",
        "hop": 632,
        "mo": "05550000001",
        "ipg": {
            "ipghtime": int(user_transaction.created_at.timestamp()),
            "ipghtran": user_transaction.id
        }
    }

    payload = {
        "hreq": json.dumps(inquiry_data),
        "hsign": ""
    }

    r = requests.request("POST", url, data=json.dumps(payload))

    return r.json()


def get_link(request):
    # blacklist countries for online payment
    user_country = DbIpCity.get(get_client_ip(request), api_key='free').country
    if user_country in settings.PAYMENT_BLACK_LIST:
        raise ValidationError(_("online payment is not available in your country"))
    # validate request
    if request.data.get("order_id") in ("", None):
        raise ValidationError(_("order_id is incorrect or missed"))

    if request.data.get("payment_type") in ("", None):
        raise ValidationError(_("payment type is incorrect or missed"))

    # find related order
    order = Order.objects.get(id=request.data.get("order_id"))

    # check for unknown transaction for current order
    unknown_transaction = PaymentTransaction.objects.filter(order=order, status=UNKNOWN)
    if len(unknown_transaction) != 0:
        raise ValidationError(_("You have an unknown transaction. You can Inquire the status or proceed to profile. "
                                "You can contact support with WhatsApp on 908507000700."))

    # create a transaction
    trans = PaymentTransaction.objects.create(order=order)
    trans.transaction_id = trans.uuid
    trans.save()

    amount = order.amount
    payment_type = request.data.get("payment_type")

    if payment_type == PARTIAL:
        amount = amount * 0.2

    # make payment data
    payment_data = {
        "lang": "TR",
        "ver": "v1",
        "hi": 1919,
        "htran": trans.id,
        "htime": int(trans.created_at.timestamp()),
        "hkey": "40efc1c1-f7f3-44bf-bdb5-fb54bf285648",
        "hop": 8060,
        "mo": "05550000001",
        "ao": int(amount * 100),
        "pid": "0",
        "pcid": "0",
        "currency": "978",
        "mrchinf": {
            "merch": 23,
            "msurl": settings.PAYMENT_CALLBACK_URL + "/api/v1/pay/callback/{}/{}/".format(payment_type, trans.uuid),
            "mfurl": settings.PAYMENT_CALLBACK_URL + "/api/v1/pay/callback/{}/{}/".format(payment_type, trans.uuid),
        }
    }

    # get payment link
    r = requests.post(
        "{}/exts/payment/0/v1/999/1".format(settings.SUPER_PAY_URL),
        headers={
            "ContentType": "application/json",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "hreq": json.dumps(payment_data),
                "hsign": ""
            }
        ),
    )

    r = r.json()

    payment_link = json.loads(r["hresp"]).get("secure3DUrl", None)

    if payment_link is None:
        raise ValidationError(_("payment call error"))

    return {
        "PaymentLink": payment_link
    }


def validate_payment(request, payment_type, transaction_uid):
    # validate request
    if transaction_uid in ("", None):
        raise ValidationError(_("transaction id is incorrect or missed"))

    # find transaction
    trans = PaymentTransaction.objects.get(uuid=transaction_uid)

    # find related order
    order = trans.order

    # inquiry transaction
    r = transaction_inquiry(trans.transaction_id)
    trans.transaction_response = r

    order_amount = order.amount

    if payment_type == PARTIAL:
        order_amount = order_amount * 0.2

    if r["hstat"] == 3017 or r["hstat"] == 1201:
        trans.status = UNKNOWN
        trans.save()
        raise ValidationError(_("You have an unknown transaction. You can Inquire the status or proceed to profile. "
                                "You can contact support with WhatsApp on 908507000700."),
                              UNKNOWN)

    if r["hstat"] != 0:
        trans.status = FAILED
        trans.save()
        raise ValidationError(_("Payment Failed. You can proceed to profile retry payment."), FAILED)

    trans.status = SUCCESS
    trans.save()

    order.status = WAITING_FOR_RECEIVING_FIRST_DOSE
    order.payment_type = payment_type
    order.payment_date = datetime.datetime.now()
    order.paid_amount = order_amount
    order.save()

    otp = OTP.objects.create(user=order.user)

    order.user.email_user(
        "Tourist.health",
        "Hi there,\n We have successfully received your payment for order number {}."
        "\n Please use the link below to"
        " login to your profile and complete your order and book your vaccination."
        "https://tourist.health/auth/login?otp={}&email={}".format(
            order.code, otp.code, order.user.email
        ),
        "no-reply@tourist.health",
    )


def payment_by_exchange(request):
    if request.data.get("exchange_id") in (None, ""):
        raise ValidationError(_("exchange is not valid"))

    if request.data.get("user_id") in (None, ""):
        raise ValidationError(_("user is not valid"))

    if request.data.get("order_id") in (None, ""):
        raise ValidationError(_("order is not valid"))

    user = User.objects.get(id=int(request.data.get("user_id")))

    try:
        exchange = Exchange.objects.get(
            id=int(request.data.get("exchange_id")),
            users=user
        )
    except Exception as e:
        raise ValidationError(_("user haven't access to specified exchange"))

    try:
        order = Order.objects.get(
            id=int(request.data.get("order_id")),
            payment_type=None
        )
    except Order.DoesNotExist:
        raise ValidationError(_("order doesn't exist"))

    with transaction.atomic():
        # set transaction
        trans = PaymentTransaction.objects.create()
        trans.status = SUCCESS
        trans.exchange = exchange
        trans.user = user
        trans.order = order
        trans.save()

        # set order
        order.status = WAITING_FOR_RECEIVING_FIRST_DOSE
        order.payment_type = EXCHANGE
        order.payment_date = datetime.datetime.now()
        order.paid_amount = order.amount
        order.save()

    otp = OTP.objects.create(user=order.user)

    order.user.email_user(
        "Tourist.health",
        "Hi there,\n We have successfully received your payment for order number {} from {} exchange "
        "store.\n Please use the link below to"
        " login to your profile and complete your order and book your vaccination."
        "https://tourist.health/auth/login?otp={}&email={}".format(
            order.code, exchange.name, otp.code, order.user.email
        ),
        "no-reply@tourist.health",
    )


def payment_by_usdt(request):
    usdt_token = request.data.get("usdt_token", None)
    if usdt_token is None:
        raise ValidationError(_("please insert payment token"))
    order = Order.objects.get(user=request.user)
    if order.usdt_token not in ("", None):
        raise ValidationError(_("a usdt transacion exist"))
    order.usdt_token = usdt_token
    order.save()
    trans = PaymentTransaction.objects.create()
    trans.transaction_id = trans.uuid
    trans.order = order
    trans.transaction_request = usdt_token
    trans.save()


def create_usdt_transaction(request):
    try:
        order = Order.objects.get(user=request.user, status=WAITING_FOR_PAY)
    except Exception as e:
        raise ValidationError(_("not found"))

    if order.usdt_address not in ("", None):
        raise ValidationError(_("you have an usdt address already"))

    usdt_amount = exchange_euro_to_usdt(order.amount)

    create_cryptom_data = {
        "order": {
            "order_id": str(order.uuid),
            "service_name": "vaccine",
            "network_type": "NETWORK_TYPE_TRON",
            "callback_url": settings.CRYPTO_CALLBACK_URL + reverse("update_usdt_payment", kwargs={
                "order_id": order.uuid
            }) + "?token={}".format(settings.EXTERNAL_API_KEY),
            "amount": usdt_amount
        }
    }

    cryptom_response = requests.post(
        settings.CRYPTOM_API_URL + settings.CRYPTOM_CREATE_TRANSACTION, json=create_cryptom_data)

    cryptom_parsed = cryptom_response.json()

    order.usdt_address = cryptom_parsed["address"]
    order.usdt_payment_id = cryptom_parsed["payment_id"]
    order.save()


def update_usdt_transaction(request, order_id):
    try:
        order = Order.objects.get(uuid=order_id)
    except Exception as e:
        raise ValidationError(_("not found"))

    amount = request.data.get("value")
    if amount in (None, ""):
        raise ValidationError(_("not found"))
    transaction_id = request.data.get("id")
    if transaction_id in (None, ""):
        raise ValidationError(_("not found"))
    order_transactions = PaymentTransaction.objects.filter(order=order, status=SUCCESS)
    for order_transaction in order_transactions:
        try:
            parsed_response = json.loads(order_transaction.transaction_response)
        except Exception as e:
            continue
        order_transaction_id = parsed_response.get("id")
        if order_transaction_id is not None:
            if order_transaction_id == transaction_id:
                raise ValidationError(_("transaction found"))

    amount = exchange_usdt_to_euro(float(amount))

    with transaction.atomic():
        if amount + order.paid_amount >= order.amount:
            order.status = WAITING_FOR_RECEIVING_FIRST_DOSE
        order.payment_type = USDT
        order.payment_date = datetime.datetime.now()
        order.paid_amount += amount
        usdt_transaction = PaymentTransaction.objects.create(order=order)
        usdt_transaction.status = SUCCESS
        usdt_transaction.transaction_response = json.dumps(request.data)
        order.save()
        usdt_transaction.save()

    if order.paid_amount >= order.amount:
        otp = OTP.objects.create(user=order.user)
        order.user.email_user(
            "Tourist.health",
            "Hi there,\n We have successfully received your payment for order number {}."
            "\n Please use the link below to"
            " login to your profile and complete your order and book your vaccination."
            "https://dev.cov19.vc/auth/login?otp={}&email={}".format(
                order.code, otp.code, order.user.email
            ),
            "no-reply@tourist.health",
        )
