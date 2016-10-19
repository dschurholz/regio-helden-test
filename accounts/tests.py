from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from django_dynamic_fixture import G

from accounts.models import Customer


class UserManagementTest(TestCase):
    def setUp(self):
        permissions = Permission.objects.filter(
            content_type__app_label='accounts',
            content_type__model='customer'
        )
        passwd = "testtest"
        self.user_1 = G(User, username="test1", email="test1@gmail.com")
        self.user_1.is_staff = True
        self.user_1.set_password(passwd)
        self.user_1.user_permissions.set(permissions)
        self.user_1.save()
        self.user_2 = G(User, username="test2", email="test2@gmail.com")
        self.user_2.is_staff = True
        self.user_2.set_password(passwd)
        self.user_2.user_permissions.set(permissions)
        self.user_2.save()
        self.customer = G(
            Customer, iban="DE21301204000000015228", created_by=self.user_1)
        self.customer.save()

    def test_customer_creation_allowed(self):
        self.client.force_login(
            self.user_1, backend='django.contrib.auth.backends.ModelBackend')
        add_customer_url = reverse('admin:accounts_customer_add')
        response = self.client.post(add_customer_url, {
            "first_name": "Cust",
            "last_name": "Omer",
            "iban": "DE44500105175407324931"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.all().count(), 2)

    def test_customer_creation_wrong_iban(self):
        self.client.force_login(
            self.user_1, backend='django.contrib.auth.backends.ModelBackend')
        add_customer_url = reverse('admin:accounts_customer_add')
        response = self.client.post(add_customer_url, {
            "first_name": "Cust",
            "last_name": "Omer",
            "iban": "WRONGIBAN"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.all().count(), 1)

    def test_customer_change_allowed(self):
        self.client.force_login(
            self.user_1, backend='django.contrib.auth.backends.ModelBackend')
        change_customer_url = reverse(
            'admin:accounts_customer_change', args=(self.customer.id,))
        response = self.client.get(change_customer_url,)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(change_customer_url, {
            "first_name": "Cust",
            "last_name": "Omer",
            "iban": "DE44500105175407324931"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Customer.objects.first().iban, "DE44500105175407324931")

    def test_customer_change_not_allowed(self):
        self.client.force_login(
            self.user_2, backend='django.contrib.auth.backends.ModelBackend')
        change_customer_url = reverse(
            'admin:accounts_customer_change', args=(self.customer.id,))
        response = self.client.get(change_customer_url,)
        self.assertEqual(response.status_code, 403)

    def test_customer_delete_allowed(self):
        self.client.force_login(
            self.user_1, backend='django.contrib.auth.backends.ModelBackend')
        delete_customer_url = reverse(
            'admin:accounts_customer_delete', args=(self.customer.id,))
        response = self.client.post(
            delete_customer_url, {"post": "yes"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.all().count(), 0)

    def test_customer_delete_not_allowed(self):
        self.client.force_login(
            self.user_2, backend='django.contrib.auth.backends.ModelBackend')
        delete_customer_url = reverse(
            'admin:accounts_customer_delete', args=(self.customer.id,))
        response = self.client.get(delete_customer_url)
        self.assertEqual(response.status_code, 403)

    def test_customer_bulk_delete_allowed(self):
        self.client.force_login(
            self.user_1, backend='django.contrib.auth.backends.ModelBackend')
        changelist_customer_url = reverse('admin:accounts_customer_changelist')
        response = self.client.post(changelist_customer_url, {
            "action": "delete_selected",
            "_selected_action": [self.customer.pk],
            "post": "yes"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.all().count(), 0)

    def test_customer_bulk_delete_not_allowed(self):
        self.client.force_login(
            self.user_2, backend='django.contrib.auth.backends.ModelBackend')
        changelist_customer_url = reverse('admin:accounts_customer_changelist')
        response = self.client.post(changelist_customer_url, {
            "action": "delete_selected",
            "_selected_action": [self.customer.pk],
            "post": "yes"
        }, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Customer.objects.all().count(), 1)
