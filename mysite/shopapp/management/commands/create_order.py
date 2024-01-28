from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from shopapp.models import Order

class Command(BaseCommand):
    '''
    create order command
    '''
    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='ainur2511')
        order = Order.objects.get_or_create(
            user=user,
            delivery_address='123 Main St',
            promocode='SALE123'
        )
        self.stdout.write(f'Created order {order}')