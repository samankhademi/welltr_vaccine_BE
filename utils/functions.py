import os
import random
import re
import string
import uuid
from datetime import datetime
from typing import Optional, Match

import requests
from django.conf import settings
from django.urls.base import reverse
from oauth2_provider.models import Application
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse


def make_response(status_code, status_message, trace_message, content):
    return Response(
        data={
            "statusCode": status_code,
            "statusMessage": status_message,
            "traceMessage": trace_message,
            "content": content,
        },
        status=status_code,
    )


def get_auth_token(username, password):
    app = Application.objects.filter(name="vaccine").last()
    r = requests.post(
        "http://127.0.0.1:8000" + reverse("oauth2_provider:token"),
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": app.client_id,
            "client_secret": app.client_secret,
        },
    )
    r = r.json()
    return r


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def panel_key_required(function):
    def wrapper(self, request, *args, **kw):
        if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("page not found")
            trace_message = _("page not found")
            return make_response(status_code, status_message, trace_message, {})

        return function(self, request, *args, **kw)

    return wrapper


def external_key_required(function):
    def wrapper(self, request, *args, **kw):
        if settings.EXTERNAL_API_KEY != request.query_params.get("token"):
            status_code = status.HTTP_404_NOT_FOUND
            status_message = _("page not found")
            trace_message = _("page not found")
            return make_response(status_code, status_message, trace_message, {})

        return function(self, request, *args, **kw)

    return wrapper


def use_permission(groups):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kw):
            use_group = "".join(groups)

            #Get User Groups
            user_groups = request.user.groups.all()
            group_list = []
            for group in user_groups:
                parsed_group = str(group).split("_")
                if len(parsed_group) != 0:
                    group_list.append(parsed_group[0])
                list(set(group_list))

            group_list = "".join(group_list)

            #User Redirect
            if len(group_list) == 0:
                return HttpResponseRedirect(reverse("panel:login"))
            # elif use_group in group_list and use_group == "NURSE":
            elif group_list == "NURSE":
                return HttpResponseRedirect(reverse("panel:order_list"))
            elif group_list == "SHROFF":
                return HttpResponseRedirect(reverse("panel:order_search"))
            else:
                return HttpResponseRedirect(reverse("panel:login"))

            return HttpResponse(status=404)
        return wrapper
    return decorator


def is_email_valid(email: str) -> Optional[Match[str]]:
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)


def is_duplicate(elements):
    for elem in elements:
        if elements.count(elem) > 1:
            return True
    return False


def get_file_path(instance, filename):
    current_date = datetime.today().strftime('%Y-%m-%d')
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('passports/{}'.format(current_date), filename)


def get_formatted_log(path, error_code, message, user):
    return {
        "path": path,
        "code": error_code,
        "message": message,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": user
    }


def get_client_ip(request):
    true_client_ip = request.META.get('HTTP_True_Client_IP')
    cf_connecting_ip = request.META.get('HTTP_CF_Connecting_IP')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if true_client_ip:
        ip = true_client_ip
    elif cf_connecting_ip:
        ip = cf_connecting_ip
    elif x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
