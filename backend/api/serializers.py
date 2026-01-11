from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Purchase, Voucher, Ecommerce

class PurchaseSerializer(serializers.ModelSerializer):
    voucher_identifier = serializers.CharField(write_only=True, required=False)
    security_code = serializers.CharField(write_only=True, required=False)
    ecommerce_api_key = serializers.CharField(write_only=True, required=False) # passed in body or header?

    class Meta:
        model = Purchase
        fields = ['id', 'order_id', 'amount', 'status', 'timestamp', 'voucher_identifier', 'security_code', 'ecommerce_api_key']
        read_only_fields = ['id', 'status', 'timestamp']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
