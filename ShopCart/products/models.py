from django.db import models
from django.core.validators import MinValueValidator
class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    image = models.CharField(max_length=160)
    class Meta: ordering = ['id']
    def __str__(self): return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.CharField(max_length=160, help_text='Local static path, e.g. images/iphone16.png')
    stock = models.PositiveIntegerField(default=15)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['id']
        constraints = [models.CheckConstraint(condition=models.Q(price__gt=0), name='positive_product_price')]
    def __str__(self): return self.name
