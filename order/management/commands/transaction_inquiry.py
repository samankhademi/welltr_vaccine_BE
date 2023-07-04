import os

from django.core.management import BaseCommand

from payment import service
from order.models import FULL
from payment.models import PaymentTransaction, UNKNOWN


class Command(BaseCommand):
    help = 'Inquiry all unknown transactions'

    def handle(self, *args, **options):

        unknown_transactions = PaymentTransaction.objects.filter(status=UNKNOWN)
        for unknown_transaction in unknown_transactions:
            try:
                service.validate_payment({}, FULL, unknown_transaction.uuid)
            except Exception as e:
                self.stdout.write(self.style.ERROR('error : "%s"' % str(e)))
                pass
            self.stdout.write(self.style.SUCCESS('Inquiry successfully called for "%s"' % unknown_transaction.id))

