from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q

from order.models import Order, WAITING_FOR_PAY
from exchange.models import Exchange
from payment.models import PaymentTransaction
from payment.serializers import PaymentTransactionSerializer
from exchange.serializers import ExchangeSerializer, ExchangeUserSerializer
from order.serializers import OrderSerializer
from order.models import Order, OPEN, WAITING_FOR_SETTING_FIRST_DOSE, WAITING_FOR_RECEIVING_FIRST_DOSE, \
    WAITING_FOR_SETTING_SECOND_DOSE, WAITING_FOR_RECEIVING_SECOND_DOSE, DONE

from django.utils.translation import ugettext_lazy as _


def get_exchange_list():
    exchanges = Exchange.objects.all()
    exchanges_serializer = ExchangeSerializer(exchanges, many=True)
    return exchanges_serializer.data


def get_user_exchange_id(id):
    exchange_set = Exchange.objects.all()
    exchange_user = id
    if exchange_user not in (None, ""):
        exchange_set = exchange_set.filter(users=exchange_user)
        exchange_user_serializer = ExchangeUserSerializer(exchange_set, many=True)
        result = exchange_user_serializer.data
    else:
        result = ""
    return result


def portal_search_order(request):
    if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
        print("portal validation error")
        raise ValidationError(_("some information lost"))

    payment_id = request.data.get("payment_id")
    if payment_id not in (None, ""):
        order_set = Order.objects.all()
        order_set = order_set.filter(code=payment_id)
        order_set = order_set.filter(status=WAITING_FOR_PAY)

        exchange_user = request.data.get("exchange_user")
        if exchange_user not in (None, ""):
            exchange_id = get_user_exchange_id(exchange_user)[0]["id"]

        order_serializer = OrderSerializer(order_set, many=True)
        if len(list(order_serializer.data)) != 0:
            result = list(order_serializer.data)
            result.append({'exchange_id': exchange_id})
        else:
            result = order_serializer.data
    else:
        result = ""

    return result


def portal_exchange_transactions(request):
    if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
        raise ValidationError(_("some information lost"))

    payment_set = PaymentTransaction.objects.all()

    payment_id = request.data.get("payment_id")
    if payment_id not in (None, ""):
        payment_set = payment_set.filter(order__code=payment_id)

    exchange_user = request.data.get("exchange_user")
    if exchange_user not in (None, ""):
        payment_set = payment_set.filter(user=exchange_user)

    from_date = request.data.get("from_date")
    to_date = request.data.get("to_date")

    if from_date not in (None, "") and to_date not in (None, ""):
        from_date = request.data.get("from_date")+"T00:00:00.00"
        to_date = request.data.get("to_date")+"T23:59:59"
        payment_set = payment_set.filter(Q(created_at__range=[from_date, to_date]))

    payment_set = payment_set.order_by('-created_at')

    peyment_serializer = PaymentTransactionSerializer(payment_set, many=True)

    return peyment_serializer.data
