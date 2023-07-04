import json
from datetime import datetime, timedelta
from typing import Dict, Any

from django.core.validators import validate_email
from django.db.models import Q

import order.service as order_service
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from order.models import OPEN, WAITING_FOR_DATA_SUBMISSION, Order, VaccineType
from utils.functions import get_auth_token

from .models import OTP, Person, User, UserGroups


def send_otp(email, is_login=False):
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError(
            _("The Email you have entered does not exist. You need to register first")
        )

    email_temp = "mail_template.html"
    if is_login:
        email_temp = "login_mail_template.html"
    otp = OTP.objects.create(user=user)
    html_message = render_to_string(
        email_temp,
        {
            "link": "https://dev.cov19.vc/auth/login?otp={}&email={}".format(
                otp.code, email
            ),
            "otp": otp.code
        },
    )
    plain_message = strip_tags(html_message)
    email_title = "Tourist.health - Your Activation Link"
    if is_login:
        email_title = "Tourist.health - Your Otp"
    user.email_user(
        email_title,
        plain_message,
        "no-reply@tourist.health",
        html_message=html_message,
    )


def signup(request):
    # validate request
    if request.data.get("user") in ("", None):
        raise ValidationError(_("user is incorrect or missed"))

    if request.data.get("location") in ("", None):
        raise ValidationError(_("location is incorrect or missed"))

    if request.data.get("vaccine_type") in ("", None):
        raise ValidationError(_("vaccine_type is incorrect or missed"))

    validate_email(request.data.get("user")["email"])

    if request.data.get("user")["email"] in ("", None):
        raise ValidationError(_("email is incorrect or missed"))

    if request.data.get("user")["phone"] in ("", None):
        raise ValidationError(_("mobile number is incorrect or missed"))

    package_uid = request.data.get("package_uid")
    if package_uid in ("", None):
        raise ValidationError(_("please select a hotel package"))

    # check user exist
    try:
        user = User.objects.get(Q(email=request.data.get("user")["email"]) | Q(phone=request.data.get("user")["phone"]))
    except User.DoesNotExist:
        user = None

    if user is not None:
        raise ValidationError(
            _("user with this email or phone already exist, please login with this email")
        )

    with transaction.atomic():
        # make user
        u = User()
        user_info = request.data.get("user")
        user_info["password"] = ""
        u.full_clean(user_info)
        u.email = user_info.get("email", None)
        u.phone = user_info.get("phone", None)
        u.country = user_info.get("country", None)
        u.set_unusable_password()
        u.save()
        customer_group, created = Group.objects.get_or_create(name=UserGroups.CUSTOMER)
        u.groups.add(customer_group)

        # make persons
        persons = request.data.get("persons", [])

        if len(persons) != 0:
            for p in persons:
                person = Person()
                for field in Person._meta.get_fields():
                    if field.name not in ["id", "user", "uuid"]:
                        person.__setattr__(field.name, p.get(field.name, ""))
                person.user = u
                person.is_deleted = False
                person.deleted_at = None
                person.clean_fields()
                person.save()

        # make order
        vaccine_type = request.data.get("vaccine_type")
        if not VaccineType.objects.get(id=vaccine_type).is_available:
            raise ValidationError(
                _("your selected vaccine type is not available at the moment")
            )
        vaccine_center = request.data.get("vaccine_center")
        order_service.create_order(vaccine_type, vaccine_center, u, package_uid)

        return u


def login(request):
    # validate request
    if request.data.get("email") in ("", None):
        raise ValidationError(_("email is empty"))
    if request.data.get("otp") in ("", None):
        raise ValidationError(_("otp is incorrect or missed"))

    # validate otp
    otp = OTP.objects.filter(
        code=int(request.data.get("otp")),
        # is_used=False,
        created_at__gte=datetime.now() - timedelta(days=14),
        user__email=request.data.get("email"),
    ).last()

    if otp:
        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            raise ValidationError(
                _(
                    "The Email you have entered does not exist. You need to register first"
                )
            )
        user.set_password(request.data.get("otp"))
        user.save()
        resp = get_auth_token(user.email, request.data.get("otp"))
        otp.is_used = True
        otp.save()
        return resp

    raise ValidationError(_("otp is incorrect or expired"))


def add_person(request):
    # validate request
    if request.data.get("persons") in ([], None):
        raise ValidationError(_("persons is empty"))
    order = Order.objects.filter(user=request.user).last()
    if order and order.status not in [
        WAITING_FOR_DATA_SUBMISSION,
        OPEN,
    ]:
        raise ValidationError("you can't add person at this step")

    # make persons
    persons = request.data.get("persons", [])
    for p in persons:
        person = Person()
        for field in Person._meta.get_fields():
            if field.name not in ["id", "user", "uuid"]:
                person.__setattr__(field.name, p.get(field.name, ""))
        person.user = request.user
        person.is_deleted = False
        person.deleted_at = None
        person.clean_fields()
        person.save()


def delete_person(request):
    person_uuid = request.data.get("uuid")
    if person_uuid in (None, ""):
        raise ValidationError(_("key <uuid> is null or empty"))
    person = Person.objects.get(uuid=person_uuid)
    order = Order.objects.filter(user=request.user).last()
    if order and (
        order.status not in [WAITING_FOR_DATA_SUBMISSION, OPEN]
        or order.user.persons.count() <= 1
    ):
        raise ValidationError(_("you can't delete a person at this step"))
    if person.user == request.user:
        person.delete()
        order_service.update_order_amount(request)


def edit_person(person, request):
    person_uuid = person.get("uuid")
    name = person.get("name")
    surname = person.get("surname")
    gender = person.get("gender")
    nationality = person.get("nationality")
    passport_number = person.get("passport_number")
    passport_exp_date = person.get("passport_exp_date")
    birth_date = person.get("birth_date")
    birth_country = person.get("birth_country")
    national_id = person.get("national_id")

    if name in (None, ""):
        raise ValidationError(_("key <name> is null or empty"))
    if surname in (None, ""):
        raise ValidationError(_("key <surname> is null or empty"))
    if gender in (None, ""):
        raise ValidationError(_("key <gender> is null or empty"))
    if nationality in (None, ""):
        raise ValidationError(_("key <nationality> is null or empty"))
    if passport_number in (None, ""):
        raise ValidationError(_("key <passport_number> is null or empty"))
    if passport_exp_date in (None, ""):
        raise ValidationError(_("key <passport_exp_date> is null or empty"))
    if birth_date in (None, ""):
        raise ValidationError(_("key <birth_date> is null or empty"))
    if birth_country in (None, ""):
        raise ValidationError(_("key <birth_country> is null or empty"))
    if national_id in (None, "") and nationality == "IR":
        raise ValidationError(_("key <national_id> is null or empty"))

    person = Person()

    # Validate request base on Create or Edit action
    if person_uuid not in (None, ""):
        person = Person.objects.get(uuid=person_uuid)
        if person.user != request.user:
            raise ValidationError(_("invalid person"))
    else:
        total_person = Person.objects.filter(user=request.user)
        order_person = Order.objects.get(user=request.user).hotel_package.total_person
        if len(total_person) >= order_person:
            raise ValidationError(_("invalid person"))

    person.user = request.user
    person.name = name
    person.surname = surname
    person.gender = gender
    person.nationality = nationality
    person.passport_number = passport_number
    person.passport_exp_date = passport_exp_date
    person.birth_date = birth_date
    person.birth_country = birth_country
    person.national_id = national_id
    person.save()


def edit_person_bulk(request):
    persons = request.data.get("persons", [])
    if len(persons) == 0:
        raise ValidationError(_("invalid person"))
    with transaction.atomic():
        for person in persons:
            edit_person(person, request)
