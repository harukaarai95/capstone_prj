from django.db import models
from django.urls import reverse

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
