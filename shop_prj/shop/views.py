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
from .models import Product, ProductImage, Genre, ProductInstance, Cart
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import ProductForm, ImageForm, GenreForm
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView, ListView

def home(request):
    featured_products = Product.objects.filter(is_featured=True).prefetch_related('images')
        # pass the context
    context = {
            # 'num_items': num_items,
            # 'user_role': user_role if request.user.is_authenticated else None,
            'featured_products': featured_products,
            # 'username': username if request.user.username else None,
        }
    return render(request, 'index.html', context)

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
    
class GenreListView(LoginRequiredMixin, RoleRequiredMixin, generic.ListView):
    allowed_roles = ['STAFF', 'MASTER']
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
    
#### CUSTOMER VIEWS ###
class CustomerProductListView(generic.ListView):
    model = Product
    template_name = 'c_product_list.html'
    context_object_name = 'products'
   
    def get_queryset(self):
        on_sale_products = Product.objects.filter(status="ON_SALE")
        return on_sale_products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True)
        context['featured_total'] = context['featured_products'].count()
        context['other_products'] = Product.objects.filter(status="ON_SALE", is_featured=False)
        context['on_sale_products'] = self.get_queryset()

        genre_count = Genre.objects.annotate(product_count=Count('products')).order_by('-product_count')[:3] #top3
        context['genre_count'] = genre_count
        context['genres'] = Genre.objects.all()
        
        genre_products = []
        for genre in context['genres']:
            genre_products.append({
                'genre': genre,
                'products': genre.products.all()
            })

        context['genre_products'] = genre_products
        return context

class CustomerProductDetailView(generic.DetailView):
    model = Product
    template_name = 'c_product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all()
        return context
    
@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        amount = request.POST.get("amount")

        if amount is None:
            return JsonResponse({"success": False, "error": "Missing amount"}, status=400)

        try:
            amount = int(amount)
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid amount"}, status=400)

        cart, created = Cart.objects.get_or_create(user=request.user)

        product_instance = ProductInstance.objects.filter(cart=cart, product=product).first()

        if product_instance:

            if product_instance.status == 'In_cart':
                product_instance.amount += amount
                product_instance.save()
            else:
                ProductInstance.objects.create(
                    product=product,
                    cart=cart,
                    amount=amount,
                    status='In_cart'
                )
        else:
            ProductInstance.objects.create(
                product=product,
                cart=cart,
                amount=amount,
                status='In_cart'
            )

        print(f"Product ID: {product.id}, Amount: {amount}")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


class CustomerCartDetail(LoginRequiredMixin, TemplateView):
    template_name = 'cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            print(f"Cart for user {self.request.user.username}: {cart}")
            if cart:
                context['cart_items'] = ProductInstance.objects.filter(cart=cart, status='In_cart')
                print(f"Cart Items: {context['cart_items']}")

                context['total_price'] = sum(
                    (item.product.price * item.amount) for item in context['cart_items'] if item.product is not None
                )

            else:
                context['cart_items'] = []
                context['total_price'] = 0

        return context
    
@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        product_instance = ProductInstance.objects.filter(cart=cart, product_id=product_id, status='In_cart').first()
        if product_instance:
            product_instance.delete()

    return redirect('c_cart_detail')


@login_required
def update_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        amount = request.POST.get("amount")
        
        if amount is None:
            return JsonResponse({"success": False, "error": "Missing amount"}, status=400)

        try:
            amount = int(amount)
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid amount"}, status=400)

        cart = Cart.objects.filter(user=request.user).first()
        product_instance, created = ProductInstance.objects.get_or_create(
            cart=cart, product=product, defaults={'amount': amount}
        )
        if not created:
            product_instance.amount = amount
            product_instance.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@login_required
def purchase_item(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product_instance = get_object_or_404(ProductInstance, product__id=product_id, cart=cart)

    product_instance.status = 'Requested'
    product_instance.save()

    return redirect('order_history')

@login_required
def purchase_all(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    ProductInstance.objects.filter(cart=cart, status='In_cart').update(status='Requested')

    return redirect('order_history')

class PurchaseHistoryView(LoginRequiredMixin, ListView):
    model = ProductInstance
    template_name = 'order_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_instances = ProductInstance.objects.filter(
            cart__user=self.request.user
        ).exclude(status='In_cart').order_by('-order_date')

        context['product_instances'] = product_instances

        return context

class CustomerGenreDetailView(DetailView):
    model = Genre
    template_name = 'c_genre_detail.html'
    context_object_name = 'genre'