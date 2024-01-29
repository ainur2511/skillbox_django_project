from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    '''
    update order command
    '''
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('no order found')
            return

        products = Product.objects.all()
        for product in products:
            order.products.add(product)

        order.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully added {order.products.all()} to order {order} '))