import uuid
from django.db import models
from django.conf import settings
class Order(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=80)
    postcode = models.CharField(max_length=6)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='placed', choices=[('placed','Placed'),('processing','Processing'),('shipped','Shipped'),('delivered','Delivered')])
    payment_method = models.CharField(max_length=30, default='Cash on delivery')
    checkout_token = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return str(self.reference)
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey('products.Product',on_delete=models.PROTECT)
    name = models.CharField(max_length=160)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    @property
    def subtotal(self): return self.price*self.quantity
