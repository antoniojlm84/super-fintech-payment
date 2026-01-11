import hashlib
import time
from django.db import models
from django.contrib.auth.models import User

def generate_sha1_id(prefix=''):
    """Generates a unique SHA1 ID."""
    s = f"{prefix}{time.time()}"
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

class BaseModel(models.Model):
    id = models.CharField(max_length=40, primary_key=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_sha1_id(self.__class__.__name__)
        super().save(*args, **kwargs)

class Ecommerce(BaseModel):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True, help_text="Secret API Key used for backend-to-backend communication")
    public_key = models.CharField(max_length=255, unique=True, help_text="Public Key used in the frontend widget")
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Voucher(BaseModel):
    identifier = models.CharField(max_length=50, unique=True, help_text="The public voucher ID entered by the shopper")
    security_code = models.CharField(max_length=50, help_text="The secret code entered by the shopper")
    is_active = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=10, choices=[('percent', 'Percentage'), ('fixed', 'Fixed Amount')], default='fixed')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.identifier} ({self.value})"

class Purchase(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    ecommerce = models.ForeignKey(Ecommerce, on_delete=models.CASCADE, related_name='purchases')
    order_id = models.CharField(max_length=255) # E-commerce's own order ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional: Validated voucher/code usage
    voucher_code = models.CharField(max_length=50, null=True, blank=True)
    voucher_secret = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"

class PurchaseVoucher(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='used_vouchers')
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('purchase', 'voucher')
