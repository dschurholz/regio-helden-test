from django.contrib import admin
from django.contrib import messages

from accounts.models import Customer
from accounts.utils import get_sentinel_user


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", )
    list_display = (
        "iban", "first_name", "last_name", "created_by_email_display")
    search_fields = ("first_name", "last_name", "iban")

    def has_change_permission(self, request, obj=None):
        if (obj is not None and obj.created_by != request.user and
                obj.created_by != get_sentinel_user()):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # For single deletion
        if (obj is not None and obj.created_by != request.user and
                obj.created_by != get_sentinel_user()):
            return False
        # For multiple deletion
        if request.POST and request.POST.get('action') == 'delete_selected':
            if (Customer.objects.filter(
                    id__in=request.POST.getlist('_selected_action')).exclude(
                    created_by__in=[request.user, get_sentinel_user()]).
                    count() >= 1):
                messages.error(request, (
                    "Some of the customers were not created by you, thus you "
                    "are not allowed to delete them."
                ))
                return False
        return True

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Customer, CustomerAdmin)
