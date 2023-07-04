import logging
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.functions import make_response, get_formatted_log
from . import service


debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("info_logger")


# Create your views here.
class ExchangeListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            content = service.get_exchange_list()
            status_code = status.HTTP_200_OK
            status_message = _("Success")
            trace_message = ""
        except Exception as e:
            content = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("internal error")
            trace_message = str(e)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)


class SearchPortalOrderPayment(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        content = []
        try:
            content = service.portal_search_order(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("Sorry, some information lost")
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
        return make_response(status_code, status_message, trace_message, content)


class ListPortalExchangeTransaction(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        content = []
        try:
            content = service.portal_exchange_transactions(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("Sorry, some information lost")
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
        return make_response(status_code, status_message, trace_message, content)