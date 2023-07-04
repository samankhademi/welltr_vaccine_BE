import logging
import re

from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.views import APIView
from utils.functions import make_response, get_formatted_log
from oauth2_provider.models import AccessToken

from authentication import service
from .forms import PassportFileForm

from .models import Person

debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("info_logger")


@protected_resource()
@csrf_exempt
def upload_view(request, uuid):
    if request.method == "POST":
        try:
            passport_form = PassportFileForm(request.POST, request.FILES)
            if passport_form.is_valid():
                app_tk = request.META["HTTP_AUTHORIZATION"]
                m = re.search('(Bearer)(\s)(.*)', app_tk)
                app_tk = m.group(3)
                acc_tk = AccessToken.objects.get(token=app_tk)
                user = acc_tk.user
                p = Person.objects.get(uuid=uuid, user=user)
                if p.passport_image in (None, ""):
                    p.passport_image = passport_form.cleaned_data.get("passport_image")
                    p.save()
                    return HttpResponse("uploaded", status=status.HTTP_201_CREATED)
                debug_logger.debug(get_formatted_log(
                        request.path,
                        status.HTTP_400_BAD_REQUEST,
                        "person and user not found",
                        request.user
                    )
                )
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    passport_form.errors,
                    request.user
                )
            )
            return HttpResponse(passport_form.errors.get("passport_image"), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
            return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            user = service.signup(request)
            service.send_otp(user.email)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
            content = {}

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_message = str(e.message)
            if hasattr(e, "message"):
                status_message = e.message
            trace_message = str(e)
            debug_logger.debug(get_formatted_log(
                    request.path,
                    status.HTTP_400_BAD_REQUEST,
                    str(e),
                    request.user
                )
            )
            content = {}

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
            content = {}

        return make_response(status_code, status_message, trace_message, content)


class OTPView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            service.send_otp(request.data.get("email"), True)
            status_code = status.HTTP_200_OK
            status_message = "otp sent successfully"
            trace_message = ""
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


class LoginView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
            content = service.login(request)

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


class AddPersonView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            service.add_person(request)
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
            status_message = _("Sorry, some information is incorrect")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})


class DeletePersonView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            service.delete_person(request)
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
            status_message = _("Sorry, some information is incorrect")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, {})


class EditPersonView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            content = service.edit_person(request.data, request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except ValidationError as e:
            content = {}
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
            content = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("Sorry, some information is incorrect")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)


class EditPersonBulkView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            content = service.edit_person_bulk(request)
            status_code = status.HTTP_200_OK
            status_message = ""
            trace_message = ""
        except ValidationError as e:
            content = {}
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
            content = {}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_message = _("Sorry, some information is incorrect")
            trace_message = str(e)
            error_logger.error(get_formatted_log(
                    request.path,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    str(e),
                    request.user
                )
            )
        return make_response(status_code, status_message, trace_message, content)
