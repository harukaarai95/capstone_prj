
from django import forms
from .models import Product, ProductImage, Genre, ProductInstance
from authentication.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pname', 'description', 'price','genre', 'status', 'is_featured']
        widgets = {
            'genre': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'genre': 'Categories',
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = ProductImage
        fields = ['image', 'alt', 'status', 'product', 'is_slider_image']
        widgets = {
            'Product': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['product'].initial = product

class GenreForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = "image"
        self.fields['name'].label = "category"

    class Meta:
        model = Genre
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered rounded', 'placeholder': 'input category name'}),
        }

class ChangeCartStatusForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['status']
        labels = {'status': 'Please slect the status.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['status'].choices = ProductInstance.ORDER_STATUS
