import random
import string

from authentication.models import OTP, Person, User
from authentication.serializers import PersonSerializer
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from order.models import (
    DONE,
    VaccineType,
    WAITING_FOR_RECEIVING_FIRST_DOSE,
    WAITING_FOR_RECEIVING_SECOND_DOSE,
    WAITING_FOR_SETTING_FIRST_DOSE,
    WAITING_FOR_SETTING_SECOND_DOSE,
    Order,
    VaccineCenter, OPEN, WAITING_FOR_PAY, Coupon, AVAILABLE, USED, HotelPackage, CurrencyExchangeRate, USDT_C,
)
from order.serializers import OrderSerializer, VaccineCenterSerializer, VaccineTypeSerializer, HotelPackageSerializer, \
    ExternalHotelPackageSerializer
from utils.functions import is_duplicate


def get_user_order(request):
    order = Order.objects.get(user=request.user)
    persons = Person.objects.filter(user=request.user)
    person_serializer = PersonSerializer(persons, many=True)
    order_serializer = OrderSerializer(order)
    order_data = order_serializer.data
    order_data["persons"] = person_serializer.data
    return order_data


def create_order(vaccine_type, vaccine_center, user, package_uid):
    vaccine_type = VaccineType.objects.get(id=vaccine_type)
    package = HotelPackage.objects.get(uuid=package_uid)
    order = Order.objects.create(
        vaccine_type=vaccine_type,
        user=user,
        amount=package.price,
        hotel_package=package
    )
    order.full_clean()
    order.save()


def edit_order(request):
    if request.data.get("vaccine_center") in ("", None):
        raise ValidationError(_("key <vaccine_center> is incorrect or missed"))
    if request.data.get("vaccine_type") in ("", None):
        raise ValidationError(_("key <vaccine_type> is incorrect or missed"))
    if not VaccineType.objects.get(id=request.data.get("vaccine_type")).is_available:
        raise ValidationError(
            _("your selected vaccine type is not available at the moment")
        )
    vaccine_center = VaccineCenter.objects.get(id=request.data.get("vaccine_center"))
    vaccine_type = VaccineType.objects.get(id=request.data.get("vaccine_type"))

    order = Order.objects.get(user=request.user)
    order.vaccine_type = vaccine_type
    order.vaccine_center = vaccine_center
    order.full_clean()
    order.save()


def get_vaccine_centers():
    vaccine_centers = VaccineCenter.objects.all()
    vaccine_centers_serializer = VaccineCenterSerializer(vaccine_centers, many=True)
    return vaccine_centers_serializer.data


def get_vaccine_types():
    vaccine_types = VaccineType.objects.all()
    vaccine_types_serializer = VaccineTypeSerializer(vaccine_types, many=True)
    return vaccine_types_serializer.data


def complete_order(request):
    if request.data.get("arrival_date") in (None, ""):
        raise ValidationError(_("key <arrival_date> is incorrect or missed"))
    order = Order.objects.get(user=request.user)
    if order.status == WAITING_FOR_SETTING_FIRST_DOSE or order.status == OPEN:
        off_amount = 0
        try:
            off_amount = coupons_inquiry(request)["total_off"]
        except:
            pass
        if off_amount != 0:
            order.is_used_coupon = True
            order.amount = order.amount - off_amount
            burn_coupons(request, order)
        order.dose1_flight_number = request.data.get("flight_number")
        order.dose1_transport_company_name = request.data.get("transport_company_name")
        order.dose1_arrival_date = request.data.get("arrival_date")
        order.status = WAITING_FOR_PAY
        order.save()
    elif order.status == WAITING_FOR_SETTING_SECOND_DOSE:
        order.dose2_flight_number = request.data.get("flight_number")
        order.dose2_transport_company_name = request.data.get("transport_company_name")
        order.dose2_arrival_date = request.data.get("arrival_date")
        order.status = WAITING_FOR_RECEIVING_SECOND_DOSE
        order.save()
    else:
        raise ValidationError(_("some information lost"))


def portal_get_order_list(request):

    if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
        raise ValidationError(_("some information lost"))

    order_set = Order.objects.all()

    payment_type = request.data.get("payment_type")
    if payment_type not in (None, ""):
        if payment_type == "UNPAID":
            payment_type = None
        order_set = order_set.filter(payment_type=payment_type)

    order_id = request.data.get("order_id")
    if order_id not in (None, ""):
        order_set = order_set.filter(id=int(order_id))

    user_email = request.data.get("user_email")
    if user_email not in (None, ""):
        order_set = order_set.filter(user__email__contains=user_email)

    vaccine_center = request.data.get("vaccine_center")
    if vaccine_center not in (None, ""):
        order_set = order_set.filter(vaccine_center=vaccine_center)

    vaccine_type = request.data.get("vaccine_type")
    if vaccine_type not in (None, ""):
        order_set = order_set.filter(vaccine_type=vaccine_type)

    status = request.data.get("status")
    if status not in (None, ""):
        order_set = order_set.filter(status=status)

    mobile = request.data.get("mobile")
    if mobile not in (None, ""):
        order_set = order_set.filter(user__phone__contains=mobile)

    hotel_name = request.data.get("hotel_name")
    if hotel_name not in (None, ""):
        order_set = order_set.filter(hotel_package__hotel_name__contains=hotel_name)

    nights_num = request.data.get("duration")
    if nights_num not in (None, ""):
        order_set = order_set.filter(hotel_package__nights_num=nights_num)

    from_date = request.data.get("from_date")
    to_date = request.data.get("to_date")

    if from_date not in (None, "") and to_date not in (None, ""):
        order_set = order_set.filter(
            Q(dose1_arrival_date__range=[from_date, to_date])
            | Q(dose2_arrival_date__range=[from_date, to_date])
        )

    order_serializer = OrderSerializer(order_set, many=True)

    return order_serializer.data


def portal_edit_order(request):

    if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
        raise ValidationError(_("some information lost"))

    if request.data.get("order_id") in (None, ""):
        raise ValidationError(_("key <order_id> is incorrect or missed"))

    if request.data.get("status") in ("", None):
        raise ValidationError(_("key <status> is incorrect or missed"))

    if request.data.get("vaccine_type") in ("", None):
        raise ValidationError(_("key dose1_vaccine_type is incorrect or missed"))

    if request.data.get("vaccination_date") in ("", None):
        raise ValidationError(_("key <dose1_vaccination_date> is incorrect or missed"))

    print("I AM HEREEEEEEEE")
    order = Order.objects.get(id=int(request.data.get("order_id")))
    vaccine_type = VaccineType.objects.get(uuid=request.data.get("vaccine_type"))

    order.dose1_vaccine_type = vaccine_type
    order.dose1_vaccination_date = request.data.get("vaccination_date")
    order.dose1_next_vaccination_date = request.data.get("next_vaccination_date")
    order.status = request.data.get("status")
    order.save()
    user = User.objects.get(id=order.user_id)
    otp = OTP.objects.create(user=user)
    user.email_user(
        "Tourist.health",
        "Hi there,\n You have successfully received your first dose. Please login to your profile and book your "
        "second dose by entering your flight information.\n You can click on the following link to login to your "
        "profile "
        "https://dev.cov19.vc/auth/login?otp={}&email={}\n otp: {}".format(
            otp.code, user.email, otp.code
        ),
        "no-reply@tourist.health",
    )
    return


def update_order_amount(request):
    order = Order.objects.get(user=request.user)
    persons = Person.objects.filter(user=request.user)
    order.amount = len(persons) * settings.ORDER_AMOUNT
    order.save()


def portal_get_order_detail(request):

    if settings.PORTAL_API_KEY != request.headers.get("API-KEY"):
        raise ValidationError(_("some information lost"))

    if request.data.get("order_id") in (None, ""):
        raise ValidationError(_("some information lost"))

    order = Order.objects.get(id=int(request.data.get("order_id")))
    persons = Person.objects.filter(user=order.user)
    person_serializer = PersonSerializer(persons, many=True)
    order_serializer = OrderSerializer(order)
    order_data = order_serializer.data
    order_data["persons"] = person_serializer.data
    return order_data


def exchange_lira_to_eur(lira: float) -> float:
    import requests

    resp = requests.get(
        "http://api.exchangeratesapi.io/v1/latest?access_key=1cdee7e171a49d92ff4234f18d5bb467&symbols=TRY,EUR&format=1"
    )
    ratio = resp.json()["rates"]["TRY"]
    return lira / ratio


def coupons_inquiry(request):
    pins = request.data.get("pins", None)
    if pins in (None, ""):
        raise ValidationError(_("some information lost"))

    if is_duplicate(pins):
        raise ValidationError(_("can not duplicate pins"))

    related_order = Order.objects.get(user=request.user)

    if related_order.wrong_coupon_count == settings.MAX_WRONG_PIN_NUMBER - 1:
        raise ValidationError(_("Too many attempts. You cannot use coupons anymore"))

    related_persons = Person.objects.filter(user=request.user)
    if len(pins) > len(related_persons):
        raise ValidationError(_("pins can't be greater than order related persons"))

    coupons = []

    for pin in pins:
        try:
            coupon = Coupon.objects.get(pin=pin, status=AVAILABLE)
            coupons.append(coupon)
        except Exception as e:
            related_order.wrong_coupon_count += 1
            related_order.save()
            raise ValidationError(_("invalid pin, you have {} opportunities to enter pins".format(
                settings.MAX_WRONG_PIN_NUMBER - related_order.wrong_coupon_count
            )))

    total_off = 0

    for coupon in coupons:
        total_off += coupon.off_percent

    related_order.wrong_coupon_count = 0
    related_order.save()

    return {
        "total_off": total_off
    }


def search_package(request, is_external=False):
    if is_external:
        api_key = request.META.get('HTTP_API_KEY', None)
        api_caller = settings.API_KEYS.get(api_key, None)
        if api_caller is None:
            raise ValidationError(_("not found"))
    packages = HotelPackage.objects.all()
    total_person = request.query_params.get("total_person", None)
    if total_person is not None:
        packages = packages.filter(total_person=int(total_person))

    hotel_name = request.query_params.get("hotel_name", None)
    if hotel_name is not None:
        packages = packages.filter(hotel_name=hotel_name)

    nights_num = request.query_params.get("nights_num", None)
    if nights_num is not None:
        packages = packages.filter(nights_num=int(nights_num))

    price = request.query_params.get("price", None)
    if price is not None:
        packages = packages.filter(price=float(price))

    total_person = request.query_params.get("total_person", None)
    if total_person is not None:
        packages = packages.filter(total_person=int(total_person))

    if is_external:
        packages_serializer = ExternalHotelPackageSerializer(packages, many=True)
    else:
        packages_serializer = HotelPackageSerializer(packages, many=True)

    return packages_serializer.data


def burn_coupons(request, order):
    pins = request.data.get("pins", None)
    for pin in pins:
        coupons = Coupon.objects.get(pin=pin, status=AVAILABLE)
        coupons.status = USED
        coupons.order = order
        coupons.save()


def get_hotel_package():
    hotel_package = HotelPackage.objects.all()
    hotel_package_serializer = HotelPackageSerializer(hotel_package, many=True)
    return hotel_package_serializer.data


def exchange_euro_to_usdt(amount):
    usdt_exchange_rate = CurrencyExchangeRate.objects.get(currency_name=USDT_C).exchange_rate
    return round(usdt_exchange_rate * amount, 2)


def exchange_usdt_to_euro(amount):
    usdt_exchange_rate = CurrencyExchangeRate.objects.get(currency_name=USDT_C).exchange_rate
    return round(amount / usdt_exchange_rate, 2)

