import os
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.heic', ".heif"]
    if value.size > 21000000:
        raise ValidationError(_("File siz must be under 20 MB"))
    if not ext.lower() in valid_extensions:
        raise ValidationError(_("File format is not supported. Please upload images and pdf files only"))


class PassportFileForm(forms.Form):
    passport_image = forms.FileField(validators=[validate_file_extension])

