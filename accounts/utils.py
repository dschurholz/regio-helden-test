from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model


def make_new_user_staff(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' and not user.is_staff:
        user.is_staff = True
        permissions = Permission.objects.filter(
            content_type__app_label='accounts',
            content_type__model='customer'
        )
        user.user_permissions.set(permissions)
        user.save()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
