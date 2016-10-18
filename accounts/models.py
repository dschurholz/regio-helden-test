from django.db import models
from django.conf import settings

from django_iban.fields import IBANField

from accounts.utils import get_sentinel_user


class Customer(models.Model):
    first_name = models.CharField(max_length=32, db_index=True)
    last_name = models.CharField(max_length=32, db_index=True)
    iban = IBANField(
        unique=True,
        help_text="Up to 34 chars bank account number, depends on country.")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET(get_sentinel_user),
        related_name='customers_added')

    def __str__(self):
        return " ".join([self.first_name, self.last_name])

    def created_by_email_display(self):
        if self.created_by == get_sentinel_user():
            return '(DELETED)'
        return self.created_by.email
    created_by_email_display.short_description = 'created by'
    created_by_email_display.admin_order_field = 'created_by__email'
