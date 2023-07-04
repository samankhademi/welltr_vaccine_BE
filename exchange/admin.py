from django.contrib import admin
from django.contrib.admin import display

from exchange.models import Exchange


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["name", "state", "address", "get_users", "phone"]
    search_fields = ("name", "state", "phone",)

    @display(description="EXCHANGE USERS")
    def get_users(self, obj):
        return " - ".join([user.email for user in obj.users.all()])


# Register your models here.
admin.site.register(Exchange, ExchangeAdmin)
