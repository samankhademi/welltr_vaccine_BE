import qrcode
import logging
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.urls import reverse
from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from six import BytesIO

from utils.functions import make_response, get_formatted_log
from order import service
from django.utils.translation import ugettext_lazy as _


info_logger = logging.getLogger("info_logger")
debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("info_logger")


# Create your views here.
class GetOrderView(APIView):
    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            content = service.get_user_order(request)
            status_code = status.HTTP_200_OK
            status_message = _("Success")
            trace_message = ""
        except Exception as e:
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("Sorry, order not found")
            trace_message = str(e)
            content = {}
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)


class EditOrderView(APIView):
    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            service.edit_order(request)
            status_code = status.HTTP_200_OK
            status_message = ""
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


class VaccineCenterView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            vaccine_centers = service.get_vaccine_centers()
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
            vaccine_centers = {}
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
        return make_response(status_code, status_message, trace_message, vaccine_centers)


class VaccineTypeView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            vaccine_types = service.get_vaccine_types()
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
            vaccine_types = {}
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
        return make_response(status_code, status_message, trace_message, vaccine_types)


class CompleteOrderView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            service.complete_order(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = _("Sorry, some information lost")
            trace_message = str(e)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})


class ListPortalOrderView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        content = []
        try:
            content = service.portal_get_order_list(request)
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


class EditPortalOrderView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            service.portal_edit_order(request)
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
        return make_response(status_code, status_message, trace_message, {})


class PortalGetOrderView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            content = service.portal_get_order_detail(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("Sorry, order not found")
            trace_message = str(e)
            content = {}
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)


class CouponsInquiry(APIView):
    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            content = service.coupons_inquiry(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
            status_code = status.HTTP_404_NOT_FOUND
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
        return make_response(status_code, status_message, trace_message, content)


class HotelPackageView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        try:
            content = service.search_package(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
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
        return make_response(status_code, status_message, trace_message, content)


class ExternalHotelPackageView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        try:
            content = service.search_package(request, is_external=True)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = str(e)
            trace_message = str(e)
            content = {}
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)


def generate_labs_qr(request, order_id):
    url = request.get_host() + reverse("panel:order_detail", kwargs={"id": order_id})
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/jpg")
    return response


def generate_general_qr(request, user_text):
    img = qrcode.make(user_text)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/jpg")
    return response
