from rest_framework import serializers

from payment.models import PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        exclude = []
        depth = 1
