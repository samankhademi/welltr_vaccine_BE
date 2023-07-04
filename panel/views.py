import logging
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from utils.functions import use_permission, get_formatted_log

from order.models import DONE, WAITING_FOR_RECEIVING_SECOND_DOSE
from .forms import FilterForm, TransForm, SearchForm
import requests
import json
import datetime
from rest_framework import status

token_key = "987de982kjhssss98733"

users = [
    {
        "username": "test",
        "password": "test"
    }
]

order_status = [
    {
        "OPEN": "open",
        "WAITING_FOR_PAY": "Waiting for Payment",
        "WAITING_FOR_RECEIVING_FIRST_DOSE": "Waiting for check in",
        "DONE": "Completed"
        # "WAITING_FOR_DATA_SUBMISSION": "Waiting For Data Submission",
        # "FULL_PAID": "Full Paid",
        # "WAITING_FOR_PAY": "Waiting for pay",
        # "PAID_20_PERCENT": "Paid 20 Percent",
        # "WAITING_FOR_SETTING_FIRST_DOSE": "Dose 1 not set",
        # "WAITING_FOR_RECEIVING_FIRST_DOSE": "Dose 1 not received",
        # "WAITING_FOR_SETTING_SECOND_DOSE": "Dose 2 not set",
        # "WAITING_FOR_RECEIVING_SECOND_DOSE": "Dose 2 not received",
        # "DONE": "Order Completed"
    }
]

payment_status = [
    {
        "": "Not Paid",
        "FULL": "Paid Online",
        "EXCHANGE": "Paid by Exchange",
        "USDT": "Paid by USDT"
    }
]

NURSE = "NURSE"
SHROFF = "SHROFF"

debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("info_logger")


# Create your views here.
def error500(request):
    return render(request, "panel/500.html")


def login(request):
    if request.method == "POST":
        response_code = 0
        message = {"message": "", "token": {}}
        username = request.POST['username']
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None and \
                (len(user.groups.filter(name=NURSE)) != 0 or len(user.groups.filter(name=SHROFF)) != 0):
            django_login(request, user)
            message["message"] = "welcome!"
            return HttpResponse(json.dumps(message), status=200, content_type="application/json")

        message["message"] = "authentication error"

        if response_code == 401:
            message["message"] = "your username or password is incorrect"

        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_400_BAD_REQUEST,
            message["message"],
            request.user
        ))

        return HttpResponse(json.dumps(message), status=400, content_type="application/json")

    return render(request, "user/login.html")


@use_permission(["SHROFF"])
def labs(request):
    return redirect("panel:order_list")


def logout(request):
    django_logout(request)
    return redirect("panel:login")


@login_required
def order_list(request):
    # Request String
    requests_string = settings.PANEL_SERVICE_URL + '/api/v1/order/portal/list/'

    # Filtering
    try:
        filter_form = FilterForm(request.GET)
    except Exception as e:
        return redirect("panel:500")

    # Request Json
    request_json = {}

    request_json["API-KEY"] = settings.PORTAL_API_KEY
    if request.GET.get("order_id", None):
        request_json["order_id"] = request.GET.get("order_id")

    if request.GET.get("user_email", None):
        request_json["user_email"] = request.GET.get("user_email")

    if request.GET.get("mobile", None):
        request_json["mobile"] = request.GET.get("mobile")

    if request.GET.get("vaccine_center", None):
        request_json["vaccine_center"] = request.GET.get("vaccine_center")

    if request.GET.get("vaccine_type", None):
        request_json["vaccine_type"] = request.GET.get("vaccine_type")

    if request.GET.get("hotel_name", None):
        request_json["hotel_name"] = request.GET.get("hotel_name")

    if request.GET.get("duration", None):
        request_json["duration"] = request.GET.get("duration")

    # if request.GET.get("from_date", None) and request.GET.get('to_date', None):
    if (request.GET.get("from_date") is not None and "/" in request.GET.get("from_date")) or (
            request.GET.get("to_date") is not None and "/" in request.GET.get("to_date")):
        if request.GET.get('from_date'):
            request_json['from_date'] = str(datetime.datetime.strptime(request.GET.get('from_date'), "%d/%m/%Y").date())
        else:
            request_json['from_date'] = str(datetime.datetime.now().date() - datetime.timedelta(days=1))

        if request.GET.get('to_date'):
            request_json['to_date'] = str(datetime.datetime.strptime(request.GET.get('to_date'), "%d/%m/%Y").date())
        else:
            request_json['to_date'] = str(datetime.datetime.now().date() + datetime.timedelta(days=1))

    if request.GET.get("status", None):
        request_json["status"] = request.GET.get("status")

    if request.GET.get("payment_type", None):
        request_json["payment_type"] = request.GET.get("payment_type")

    is_invalid_response = False

    # Get Response
    try:
        response = requests.post(requests_string, json=request_json,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    if response.status_code == 400:
        is_invalid_response = True

    parsed_response = json.loads(response.content)

    if len(parsed_response['content']) >= 1:
        for order in parsed_response['content']:
            order['status_val'] = order_status[0][order['status']]
            if order['payment_type'] is not None:
                order['payment_type_val'] = payment_status[0][order['payment_type']]
                order['payment_type_class'] = "apSuccess"
            else:
                order['payment_type_val'] = "Unpaid"
                order['payment_type_class'] = "apFailed"
            if order['is_used_coupon']:
                order['discount'] = float(order['hotel_package']['price']) - float(order['paid_amount'])
            else:
                order['discount'] = "-"

    return render(request, "panel/list.html",
                  {'transactions': parsed_response, 'filter_form': filter_form,
                   'is_invalid_response': is_invalid_response})


@login_required
def order_detail(request, id):
    # Request String
    requests_string = settings.PANEL_SERVICE_URL + '/api/v1/order/portal/detail/'
    vaccine_centers_resource = settings.PANEL_SERVICE_URL + "/api/v1/order/vaccine-center/"
    vaccine_types_resource = settings.PANEL_SERVICE_URL + "/api/v1/order/vaccine-type/"

    # Request Json
    request_json = {}

    request_json["order_id"] = id

    # Get Response
    try:
        response = requests.post(requests_string, json=request_json,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    try:
        vaccine_centers = requests.post(vaccine_centers_resource,
                                        headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    parsed_response = json.loads(response.content)
    if len(parsed_response['content']) >= 1:
        parsed_response['content']['status_val'] = order_status[0][parsed_response['content']['status']]
        if parsed_response['content']['payment_type'] is not None:
            parsed_response['content']['payment_type_val'] = payment_status[0][
                parsed_response['content']['payment_type']]
        else:
            parsed_response['content']['payment_type_val'] = "Unpaid"
        parsed_response['content']['person_number'] = len(parsed_response['content']['persons'])
        parsed_response['content']['payment_remaining'] = float(parsed_response['content']['amount']) - float(
            parsed_response['content']['paid_amount'])
        if parsed_response['content']['is_used_coupon']:
            parsed_response['content']['discount'] = float(
                parsed_response['content']['hotel_package']['price']) - float(parsed_response['content']['paid_amount'])
        else:
            parsed_response['content']['discount'] = "-"

    parsed_vaccine_centers = json.loads(vaccine_centers.content)

    next_step = DONE
    if parsed_response["content"]["status"] == WAITING_FOR_RECEIVING_SECOND_DOSE:
        next_step = DONE

    # Get Vaccines
    try:
        vaccine_types_response = requests.post(vaccine_types_resource, json=request_json,
                                               headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    parsed_vaccine_types = json.loads(vaccine_types_response.content)

    return render(request, "panel/detail.html",
                  {'id': id, 'info': parsed_response, "vaccine_centers": parsed_vaccine_centers["content"],
                   "next_step": next_step, "vaccine_types": parsed_vaccine_types["content"]})


@login_required
def order_edit(request, id):
    order_edit_url = settings.PANEL_SERVICE_URL + "/api/v1/order/portal/edit/"

    order_edit_data = {
        "vaccine_type": request.POST["vaccine_type"],
        "order_id": id,
        "status": request.POST["next_step"]
    }

    if request.POST.get('vaccination_date'):
        order_edit_data['vaccination_date'] = str(
            datetime.datetime.strptime(request.POST.get('vaccination_date'), "%d/%m/%Y").date())

    try:
        response = requests.post(order_edit_url,
                                 data=order_edit_data,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    return redirect("panel:order_list")


@login_required
def scan_qr(request):
    info = "salam"
    return render(request, "panel/qr.html",
                  {'info': info})


@login_required
def exchange_transaction(request):
    # Request String
    requests_string = settings.PANEL_SERVICE_URL + '/api/v1/exchange/portal/transactions/'

    # Filtering
    try:
        filter_form = TransForm(request.GET)
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    # Request Json
    request_json = {}

    request_json["API-KEY"] = settings.PORTAL_API_KEY

    if request.user.id not in ("", None):
        request_json["exchange_user"] = request.user.id

    if request.GET.get("payment_id", None):
        request_json["payment_id"] = request.GET.get("payment_id")

    if (request.GET.get("from_date") is not None and "/" in request.GET.get("from_date")) or (
            request.GET.get("to_date") is not None and "/" in request.GET.get("to_date")):
        if request.GET.get('from_date'):
            request_json['from_date'] = str(datetime.datetime.strptime(request.GET.get('from_date'), "%d/%m/%Y").date())
        else:
            request_json['from_date'] = str(datetime.datetime.now().date() - datetime.timedelta(days=1))

        if request.GET.get('to_date'):
            request_json['to_date'] = str(datetime.datetime.strptime(request.GET.get('to_date'), "%d/%m/%Y").date())
        else:
            request_json['to_date'] = str(datetime.datetime.now().date() + datetime.timedelta(days=1))

    is_invalid_response = False

    # Get Response
    try:
        response = requests.post(requests_string, json=request_json,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    if response.status_code == 400:
        is_invalid_response = True

    parsed_response = json.loads(response.content)

    return render(request, "panel/exchange_transaction.html",
                  {'transactions': parsed_response, 'filter_form': filter_form,
                   'is_invalid_response': is_invalid_response})


@login_required
def order_search(request):
    # Request String
    requests_string = settings.PANEL_SERVICE_URL + '/api/v1/exchange/portal/search/'

    # Filtering
    try:
        filter_form = SearchForm(request.GET)
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    # Request Json
    request_json = {}

    request_json["API-KEY"] = settings.PORTAL_API_KEY

    if request.GET.get("payment_id", None):
        request_json["payment_id"] = request.GET.get("payment_id")

    if request.user.id not in ("", None):
        request_json["exchange_user"] = request.user.id

    is_invalid_response = False

    # Get Response
    try:
        response = requests.post(requests_string, json=request_json,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    if response.status_code == 400:
        is_invalid_response = True

    parsed_response = json.loads(response.content)

    if len(parsed_response['content']) >= 1:
        # +909147972432
        parsed_response['content'][0]["user"]["phone"] = parsed_response['content'][0]["user"]["phone"][:6] + "***" + \
                                                         parsed_response['content'][0]["user"]["phone"][9:]
        user_email = parsed_response['content'][0]["user"]["email"]
        user_email = user_email[:3] + "***@" + user_email.split("@")[-1]
        parsed_response['content'][0]["user"]["email"] = user_email
    return render(request, "panel/order_search.html",
                  {'result': parsed_response, 'filter_form': filter_form,
                   'is_invalid_response': is_invalid_response})


@login_required
def payment_update(request):
    # Request String
    requests_string = settings.PANEL_SERVICE_URL + '/api/v1/pay/exchange/'

    # Request Json
    request_json = {
        "exchange_id": request.POST["exchange_id"],
        "order_id": request.POST["order_id"]
    }
    if request.user.id not in ("", None):
        request_json["user_id"] = request.user.id

    # Get Response
    try:
        response = requests.post(requests_string,
                                 data=request_json,
                                 headers={'API-KEY': settings.PORTAL_API_KEY})
    except Exception as e:
        debug_logger.debug(get_formatted_log(
            request.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            str(e),
            request.user
        ))
        return redirect("panel:500")

    parsed_response = json.loads(response.content)

    return redirect("panel:exchange_transaction")
