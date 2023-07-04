from __future__ import unicode_literals

from enum import Enum
from random import randint

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.functions import get_file_path
from utils.models import BaseModel

from .managers import UserManager


class UserGroups(Enum):
    CUSTOMER = "CUSTOMER"
    SHROFF = "SHROFF"
    LAB = "LAB"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(
        _("phone number"), max_length=30, unique=True, blank=True, null=True
    )
    name = models.CharField(_("name"), max_length=150, blank=True, null=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    country = models.CharField(_("user country"), max_length=50, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


def otp_gen():
    return randint(100000, 999999)


class OTP(models.Model):
    user = models.ForeignKey(
        "authentication.User", verbose_name=_("related user"), on_delete=models.CASCADE
    )
    code = models.IntegerField(_("otp code"), default=otp_gen)
    is_used = models.BooleanField(_("has been used"), default=False)
    created_at = models.DateTimeField(
        _("created at"), editable=False, auto_now_add=True, null=True
    )

    class Meta:
        verbose_name = _("otp")
        verbose_name_plural = _("otps")


class Person(BaseModel):
    name = models.CharField(_("name"), max_length=50)
    surname = models.CharField(_("surname"), max_length=50)
    gender = models.CharField(_("gender"), max_length=50)
    nationality = models.CharField(_("nationality"), max_length=50)
    passport_number = models.CharField(_("passport number"), max_length=50)
    passport_exp_date = models.DateField(
        _("passport expiration date"), auto_now=False, auto_now_add=False
    )
    birth_date = models.DateField(_("birth date"), auto_now=False, auto_now_add=False)
    birth_country = models.CharField(_("birth country"), max_length=50)
    national_id = models.CharField(
        _("national id"), max_length=50, blank=True, null=True
    )
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("related user"),
        related_name="persons",
        on_delete=models.CASCADE,
    )
    passport_image = models.ImageField(
        _("passport image"), upload_to=get_file_path, blank=True, null=True
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")
