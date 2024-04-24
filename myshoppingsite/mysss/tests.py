from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Product


class MyTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_shop_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)

    def test_my_cart_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_cart'))
        self.assertEqual(response.status_code, 200)

    def test_purchases_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('purchases'))
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        product = Product.objects.create(name='Test Product', price=10, user=self.user)
        response = self.client.post(reverse('delete_product', args=[product.id]))
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_and_remove_from_cart(self):
        self.client.force_login(self.user)
        product = Product.objects.create(name='Test Product', price=10, user=self.user)


        response_add = self.client.get(reverse('add_to_cart', args=[product.id]))
        self.assertEqual(response_add.status_code, 302)


        response_remove = self.client.get(reverse('remove_from_cart', args=[product.id]))
        self.assertEqual(response_remove.status_code, 302)
