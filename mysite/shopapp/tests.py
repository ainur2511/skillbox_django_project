from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='test', password='qwerty')
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='test delivery address',
            promocode='test promocode',
            user=self.user
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:orders_detail', kwargs={'pk': '1'}),
        )
        received_pk = response.context['order'].pk
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(received_pk, self.order.pk)


class OrdersExportTestCase(TestCase):

    fixtures = [
        'db-fixtures.json'
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='test', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_orders = [{
            'pk': order.pk,
            'delivery_address': order.delivery_address,
            'promocode': order.promocode,
            'user': order.user,
            'products': order.products

            }
            for order in orders
        ]
        orders_data = response.json()
        print(orders_data)
        print(expected_orders)
        self.assertEqual(orders_data['orders'], expected_orders)
