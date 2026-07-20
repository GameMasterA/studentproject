from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Item


class InventoryFlowTests(TestCase):

    def test_login_page_is_available(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_authenticated_user_can_create_product(self):
        self.client.login(username='tester', password='securepass123')
        response = self.client.post(reverse('add_product'), {
            'name': 'Laptop',
            'quantity': 10,
            'price': 999.99,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(name='Laptop').exists())

    def test_unauthenticated_user_is_redirected_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
