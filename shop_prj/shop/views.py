# from django.shortcuts import render

# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin
from .decorators import role_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from authentication.models import User
from .models import Product, ProductImage, Genre
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import ProductForm, ImageForm, GenreForm
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Count

def home(request):
    return render(request, 'index.html')

@login_required
@role_required(allowed_roles=['STAFF', 'MASTER'])
def staff_home(request):
    return render(request, 'staff.html')

class CreateProductView(LoginRequiredMixin, RoleRequiredMixin, generic.CreateView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(ProductForm)

        product = context.get('product', None) or Product()

        ImageFormSet = inlineformset_factory(Product, ProductImage, form=ImageForm, extra=2)

        if product:
            context['image_formset'] = ImageFormSet(instance=product)
        else:
            context['image_formset'] = ImageFormSet()

        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        product = self.object
        ImageFormSet = inlineformset_factory(Product, ProductImage, form=ImageForm, extra=1)
        image_formset = ImageFormSet(self.request.POST, self.request.FILES, instance=product)

        if image_formset.is_valid():
            image_formset.save()

        return response

class ProductListView(LoginRequiredMixin, RoleRequiredMixin, generic.ListView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, RoleRequiredMixin, generic.DetailView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all()
        return context

@login_required
@role_required(allowed_roles=['STAFF', 'MASTER'])
def edit_product(request, pk):
    
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()


    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        image_form = ImageForm(request.POST, request.FILES, product=product)

        if product_form.is_valid():
            product_form.save()

        if 'add_image' in request.POST and image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.Product = product
            new_image.save()
            return redirect('product_edit', pk=pk)

        if 'edit_image' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ProductImage, id=image_id)
            image_form = ImageForm(request.POST, request.FILES, instance=image, product=product)
            if image_form.is_valid():
                image_form.save()
                return redirect('product_edit', pk=pk)

        if 'delete_image' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            return redirect('product_edit', pk=pk)

    else:
        product_form = ProductForm(instance=product)
        image_form = ImageForm(product=product)

    return render(request, 'product_edit.html', {
        'product': product,
        'product_form': product_form,
        'image_form': image_form,
        'images': images,
    })

class ProductDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Product
    template_name = 'product_confirm_delete.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all()
        return context

    def get_success_url(self):
        return reverse_lazy('products')
    
class CreateGenreView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Genre
    form_class = GenreForm
    template_name = 'genre_create.html'
    success_url = reverse_lazy('genres')

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)
    
class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = 'genre_list.html'
    context_object_name = 'genres'

    def get_queryset(self):
        return Genre.objects.annotate(product_count=Count('products'))
    
class GenreDetailView(LoginRequiredMixin, RoleRequiredMixin, generic.DetailView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Genre
    template_name = 'genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.get_object()
        context['image'] = genre.image
        return context
    
class EditGenreView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Genre
    form_class = GenreForm
    template_name = 'genre_update.html'
    success_url = reverse_lazy('genres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.get_object()
        context['genre_form'] = self.get_form()
        return context

class DeleteGenreView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Genre
    template_name = 'genre_confirm_delete.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('genres')