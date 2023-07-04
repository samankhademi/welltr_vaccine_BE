import logging
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.functions import make_response, panel_key_required, get_formatted_log, external_key_required

from . import service


# Create your views here.
from .models import UNKNOWN


debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("info_logger")


class GetPaymentLinkView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
            content = service.get_link(request)

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e)
            content = {}
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            content = {}
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )

        return make_response(status_code, status_message, trace_message, content)


class PaymentByUsdtView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
            service.payment_by_usdt(request)
            content = {}

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e)
            content = {}
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            content = {}
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )

        return make_response(status_code, status_message, trace_message, content)


class CallbackView(APIView):
    http_method_names = ["get"]

    def get(self, request, payment_type, transaction_uid, *args, **kwargs):
        try:
            service.validate_payment(request, payment_type, transaction_uid)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
            content = {}

        except ValidationError as e:
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e.message)
            content = {}
            order_param = ""
            if e.args[1] == UNKNOWN:
                order_param = "&payment_id={}".format(transaction_uid)
            return redirect("https://tourist.health/payment/failed/?message={}{}".format(trace_message, order_param))

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            content = {}
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
            return redirect("https://tourist.health/payment/failed/?message={}".format(status_message))

        return redirect("https://tourist.health/payment/success/?message={}".format(_("Payment Successful. You can "
                                                                                      "proceed to profile and "
                                                                                      "view your order.")))


class PaymentByExchangeView(APIView):

    @panel_key_required
    def post(self, request, *args, **kwargs):
        try:
            service.payment_by_exchange(request)
            status_code = status.HTTP_200_OK
            status_message = _("Success")
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})


class CreateUsdtTransaction(APIView):
    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            service.create_usdt_transaction(request)
            status_code = status.HTTP_200_OK
            status_message = _("Success")
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e)
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})


class UpdateUsdtTransaction(APIView):

    http_method_names = ["post"]

    @external_key_required
    def post(self, request, order_id, *args, **kwargs):
        try:
            service.update_usdt_transaction(request, order_id)
            status_code = status.HTTP_200_OK
            status_message = _("Success")
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = e.message
            trace_message = str(e)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})