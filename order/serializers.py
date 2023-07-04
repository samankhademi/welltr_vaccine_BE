from authentication.serializers import PersonSerializer
from rest_framework import serializers

from order.models import Order, VaccineCenter, VaccineType, HotelPackage, CurrencyExchangeRate, IRR


class VaccineCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineCenter
        exclude = ["created_at", "updated_at"]


class VaccineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineType
        exclude = ["created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):

    vaccine_center = VaccineCenterSerializer(read_only=True)
    amount_in_usdt = serializers.SerializerMethodField()

    def get_amount_in_usdt(self, obj):
        from .service import exchange_euro_to_usdt
        return exchange_euro_to_usdt(obj.amount)

    class Meta:
        model = Order
        exclude = ["uuid", "updated_at"]
        depth = 1


class HotelPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPackage
        exclude = ["created_at", "updated_at", "deleted_at", "is_deleted", "id"]


class ExternalHotelPackageSerializer(serializers.ModelSerializer):
    price_in_rial = serializers.SerializerMethodField()

    def get_price_in_rial(self, obj):
        currency = CurrencyExchangeRate.objects.get(currency_name=IRR)
        return currency.exchange_rate * obj.price

    class Meta:
        model = HotelPackage
        exclude = ["created_at", "updated_at", "deleted_at", "is_deleted", "id"]
