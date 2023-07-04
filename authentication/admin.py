from django.contrib import admin

from .models import OTP, Person, User


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "phone", "date_joined"]
    search_fields = ("email", "phone",)


class PersonAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "passport_number", "national_id", "user"]
    search_fields = ("name", "surname", "passport_number", "national_id", "user__email",)


class OtpAdmin(admin.ModelAdmin):
    list_display = ["user", "code", "is_used", "created_at"]
    search_fields = ("user__email", "code", "is_used", "created_at",)


admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(OTP, OtpAdmin)
