from rest_framework import serializers

from address_list import models


class AddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )

    class Meta:
        model = models.Address
        fields = ('id', 'address', 'latitude', 'longitude')
