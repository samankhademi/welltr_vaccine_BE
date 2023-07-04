from rest_framework import serializers

from authentication.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = []
