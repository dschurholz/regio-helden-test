from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", )
    list_display = ("iban", "first_name", "last_name")
    search_fields = ("first_name", "last_name", "iban")

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Customer, CustomerAdmin)
