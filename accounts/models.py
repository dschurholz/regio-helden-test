from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from django_iban.fields import IBANField


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


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
