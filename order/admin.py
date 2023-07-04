from django.contrib import admin

from .models import Order, VaccineCenter, VaccineType, Coupon, HotelPackage, CurrencyExchangeRate


class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "code", "user", "amount", "paid_amount", "payment_type"]
    search_fields = ("user__email", "code",)
    list_filter = ["status"]


class HotelPackageAdmin(admin.ModelAdmin):
    list_display = ["hotel_name", "room_type_en", "nights_num", "total_person", "price"]
    search_fields = ("nights_num", "total_person", "hotel_name", "price",)


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["currency_name", "exchange_rate"]
    search_fields = ("currency_name", "exchange_rate",)


admin.site.register(VaccineCenter)
admin.site.register(Order, OrderAdmin)
admin.site.register(VaccineType)
admin.site.register(Coupon)
admin.site.register(HotelPackage, HotelPackageAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
