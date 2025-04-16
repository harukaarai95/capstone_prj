from django.contrib import admin
from .models import Genre, Product, ProductImage

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pname', 'price', 'status', 'is_featured')
    list_filter = ('status', 'is_featured', 'genre')
    search_fields = ('pname', 'description')
    inlines = [ProductImageInline]
    filter_horizontal = ('genre',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt', 'status', 'is_slider_image')
    list_filter = ('status', 'is_slider_image')