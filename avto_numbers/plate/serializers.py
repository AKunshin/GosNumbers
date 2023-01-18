from rest_framework import serializers
from .models import GosNumber


class GosNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GosNumber
        fields = ('uuid', 'number')