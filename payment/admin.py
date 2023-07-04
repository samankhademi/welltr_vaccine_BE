from django.contrib import admin
from django.contrib.admin import display

from .models import PaymentTransaction


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ["status", "transaction_id", "get_order", "created_at", "updated_at"]
    search_fields = ("status", "transaction_id", "order__code", "user__email",)

    @display(description='Order Code')
    def get_order(self, obj):
        if obj.order is None:
            return ""
        return obj.order.code


# Register your models here.
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
