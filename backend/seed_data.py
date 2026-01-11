import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Ecommerce, Voucher

# Create Ecommerce
ecom, created = Ecommerce.objects.get_or_create(
    name="My Shop",
    defaults={
        "api_key": "TEST_API_KEY",
        "public_key": "TEST_PUB_KEY",
        "url": "http://localhost:8080"
    }
)
if created:
    print(f"Created Ecommerce: {ecom.name} with API Key: {ecom.api_key}")
else:
    print(f"Ecommerce exists: {ecom.name} with API Key: {ecom.api_key}")

# Create Voucher
voucher, created = Voucher.objects.get_or_create(
    identifier="GIFT-10",
    defaults={
        "security_code": "1234",
        "value": 10.00,
        "discount_type": "fixed"
    }
)
if created:
    print(f"Created Voucher: {voucher.identifier} Code: {voucher.security_code}")
else:
    print(f"Voucher exists: {voucher.identifier}")
