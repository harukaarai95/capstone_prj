from django.db import models
from django.urls import reverse
from django.conf import settings
import uuid

class Genre(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,  
        verbose_name=("genre name")
    )
    image = models.ImageField(upload_to='images/genres/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])

    class Meta:
        ordering = ['name']

class Product(models.Model):
    pname = models.CharField(max_length=255, unique=True, verbose_name='product')
    description = models.TextField(max_length=1000)
    price = models.IntegerField(null=True)
    genre = models.ManyToManyField(
        Genre, related_name='products'
    )
    ON_SALE = 'ON_SALE'
    OFF_SALE = 'OFF_SALE'
    STATUS_CHOICES = (
        (ON_SALE, 'ON_SALE'),
        (OFF_SALE, 'OFF_SALE'),
        )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, help_text=("Please select on_sale for sale."), default="OFF_SALE")
    is_featured = models.BooleanField(default=False, help_text="Please check this if you want to display this item in home.")
    
    def __str__(self):
        return self.pname
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)
    ON = 'ON'
    OFF = 'OFF'
    STATUS_CHOICES = (
        (ON, 'ON'),
        (OFF, 'OFF'),
        )
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, help_text=("Please select ON to display."), default="OFF")
    is_slider_image = models.BooleanField(default=False, help_text="Please check this if you want to display this item in slider.")

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Cart#{self.id}/ {self.user}'
    
class ProductInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, related_name="instances")
    order_date = models.DateField(auto_now=True)
    purchased_at = models.DateField(null=True, blank=True)
    amount = models.IntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    ORDER_STATUS = (('In_cart', 'In_cart'), ('Requested', 'Requested'), ('Confirmed', 'Confirmed'),('Delivered', 'Delivered'),)
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS,
        default='In_cart',
        blank=True,
    )
    @property #added subtotal property
    def subtotal(self):
        return self.amount * self.product.price
    
    class Meta:
        ordering = ['-order_date']

    def get_absolute_url(self):
        return reverse("cart_detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.product}(ordered on: {self.order_date})/ID:{self.id}'
