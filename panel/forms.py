from django import forms
import json

from django.utils.translation import ugettext_lazy as _

from order.service import get_vaccine_centers, get_vaccine_types, get_hotel_package


class FilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # Init Form Select
        super(FilterForm, self).__init__(*args, **kwargs)

        vaccine_center = json.loads(json.dumps(get_vaccine_centers()))
        centers = ()
        for center in vaccine_center:
            centers += ((center["id"], center["name"]),)
        self.fields['vaccine_center'].choices = centers

        # vaccine_type = [
        #     ('Astrazenca', 'Astrazenca'),
        #     ('Sputnik', 'Sputnik'),
        # ]
        vaccine_type = json.loads(json.dumps(get_vaccine_types()))
        types = ()
        for new_type in vaccine_type:
            types += ((new_type["id"], new_type["vaccine_type"]),)
        self.fields['vaccine_type'].choices = types

        status = [
            ('', 'All'),
            ('OPEN', 'Open'),
            ('WAITING_FOR_PAY', 'Waiting for Payment'),
            ('WAITING_FOR_RECEIVING_FIRST_DOSE', 'Waiting for check in'),
            ('DONE', 'Completed '),
        ]
        self.fields['status'].choices = status

        payment_type = [
            ('', 'Not Paid'),
            ('FULL', 'Paid Online'),
            ('EXCHANGE', 'Paid by Exchange'),
            ('USDT', 'Paid by USDT'),
        ]
        self.fields['payment_type'].choices = payment_type

        hotel_package = json.loads(json.dumps(get_hotel_package()))

        hotels = []
        nights = []
        for package in hotel_package:
            if package["hotel_name"] not in hotels:
                hotels.append(package["hotel_name"])
            if package["nights_num"] not in nights:
                nights.append(package["nights_num"])

        hotel_name = ()
        for hotel in hotels:
            hotel_name += ((hotel, hotel),)
        duration = ()
        for night in nights:
            duration += ((night, night),)
        self.fields['hotel_name'].choices = hotel_name
        self.fields['duration'].choices = duration

    order_id = forms.CharField(label='order_id', required=False, max_length=100,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control apText', 'placeholder': _('Order Id'), 'autocomplete': 'off',
                                   'type': 'number'}),
                               localize=True)
    user_email = forms.CharField(label='user_email', required=False, max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control apText', 'placeholder': _('User Email'),
                                     'autocomplete': 'off',
                                     'type': 'text'}),
                                 localize=True)
    mobile = forms.CharField(label='mobile', required=False, max_length=100,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control apText', 'placeholder': _('Mobile'), 'autocomplete': 'off',
                                 'type': 'text'}),
                             localize=True)

    vaccine_center = forms.ChoiceField(label='vaccine_center', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Vaccine Center'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '4'}), localize=True)

    vaccine_type = forms.ChoiceField(label='vaccine_type', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Vaccine Type'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '4'}), localize=True)

    hotel_name = forms.ChoiceField(label='hotel_name', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Hotel Name'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '4'}), localize=True)

    duration = forms.ChoiceField(label='duration', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Duration (nights)'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '4'}), localize=True)

    from_date = forms.DateField(label='from_date', required=False, input_formats=['%d/%m/%Y'],
                                # fromDate = forms.DateField(label='fromDate', required=False, validators=[check_length],
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control apText apRequired', 'id': 'from_date',
                                           'autocomplete': 'off', 'placeholder': _('Check in date (From)')}),
                                localize=True)

    to_date = forms.DateField(label='to_date', required=False, input_formats=['%Y/%m/%d'],
                              widget=forms.DateInput(
                                  attrs={'class': 'form-control apText apRequired', 'id': 'to_date',
                                         'autocomplete': 'off', 'placeholder': _('Check in date (To)')}),
                              localize=True)

    status = forms.ChoiceField(label='status', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Status'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '10'}), localize=True)

    payment_type = forms.ChoiceField(label='payment_type', required=False, widget=forms.Select(attrs={
        'class': 'selectpicker removable', 'title': _('Payment Status'), 'autocomplete': 'off',
        'data-hide-disabled': 'true', 'data-selected-text-format': 'count > 2',
        'data-size': '4'}), localize=True)


class TransForm(forms.Form):
    payment_id = forms.CharField(label='payment_id', required=False, max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control apText', 'placeholder': _('Payment Id'),
                                     'autocomplete': 'off',
                                     'type': 'text'}),
                                 localize=True)

    from_date = forms.DateField(label='from_date', required=False, input_formats=['%d/%m/%Y'],
                                # fromDate = forms.DateField(label='fromDate', required=False, validators=[check_length],
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control apText apRequired', 'id': 'from_date',
                                           'autocomplete': 'off', 'placeholder': _('From Date')}),
                                localize=True)

    to_date = forms.DateField(label='to_date', required=False, input_formats=['%Y/%m/%d'],
                              widget=forms.DateInput(
                                  attrs={'class': 'form-control apText apRequired', 'id': 'to_date',
                                         'autocomplete': 'off', 'placeholder': _('To Date')}),
                              localize=True)


class SearchForm(forms.Form):
    payment_id = forms.CharField(label='payment_id', required=False, max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control apText', 'placeholder': _('Payment Id'),
                                     'autocomplete': 'off',
                                     'type': 'text'}),
                                 localize=True)
