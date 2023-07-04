from rest_framework import serializers

from exchange.models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        exclude = ["created_at", "updated_at", "users", "deleted_at", "is_deleted", "uuid"]


class ExchangeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        exclude = ["created_at", "updated_at", "deleted_at", "is_deleted", "uuid"]
