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
from .forms import ProductForm, ImageForm, GenreForm, ChangeCartStatusForm
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView, ListView
from django.contrib import messages
from django.contrib.auth import get_user_model

def home(request):
    featured_products = Product.objects.filter(is_featured=True).prefetch_related('images')
    context = {
            'featured_products': featured_products,
        }
    return render(request, 'index.html', context)

@login_required
@role_required(allowed_roles=['STAFF', 'MASTER'])
def staff_home(request):
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    registerd_products = Product.objects.count()
    on_sale_products = Product.objects.filter(status="ON_SALE")
    featured_products = Product.objects.filter(is_featured=True).prefetch_related('images')
    other_products = Product.objects.filter(status="ON_SALE", is_featured=False)

    User = get_user_model()
    user_count = User.objects.count()

    undelivered_items = ProductInstance.objects.exclude(status='Delivered').count()
    need_to_confirm_items = ProductInstance.objects.filter(status='in_cart').count()
    need_to_ship_items = ProductInstance.objects.filter(status='confirmed').count()

    popular_products = ProductInstance.objects.filter(status='Delivered').values('product__pname', 'product').annotate(count=Count('id')).order_by('-count')[:5]
    top_5_products = [
    {'pname': item['product__pname'], 'id': item['product'], 'count': item['count']}
    for item in popular_products
    ]

    context = {
        'num_visits': num_visits,
        'registerd_products': registerd_products,
        'featured_products': featured_products,
        'on_sale_products': on_sale_products,
        'other_products': other_products,
        'user_count': user_count,
        'undelivered_items': undelivered_items,
        'need_to_confirm_items': need_to_confirm_items,
        'need_to_ship_items': need_to_ship_items,
        'top_5_products': top_5_products,
    }
    return render(request, 'staff.html', context)

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

class CartListView(LoginRequiredMixin, RoleRequiredMixin, generic.ListView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Cart
    context_object_name = 'cart_list'
    template_name = 'cart_list.html'

    def get_queryset(self):
        carts = Cart.objects.all()
        for cart in carts:
            cart.filtered_items = cart.items.exclude(status='Confirmed')
            cart.filtered_items_count = cart.filtered_items.count()
        return carts

class CartDetailView(LoginRequiredMixin, RoleRequiredMixin, generic.DetailView):
    allowed_roles = ['STAFF', 'MASTER']
    model = Cart
    template_name = 'cart_detail.html'
    context_object_name = 'cart'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.exclude(status='Delivered')
        completed_items = self.object.items.filter(status='Delivered')
        total = sum(item.subtotal for item in items)
        purchased_total = sum(item.subtotal for item in completed_items)

        context['filtered_items'] = items
        context['completed_items'] = completed_items
        context['total'] = total
        context['purchased_total'] = purchased_total
        return context

class ChangeCartStatusView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ['STAFF', 'MASTER']
    model = ProductInstance
    form_class= ChangeCartStatusForm
    template_name = 'change_cart_status.html'
    context_object_name = 'cart_status'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

    def form_valid(self, form):
        cart_item = form.save(commit=False)
        cart_item.status = form.cleaned_data['status']
        cart_item.save()
        
        if cart_item.cart and cart_item.cart.pk:
            messages.success(self.request, f"{cart_item.product.pname}'s status has been updated.")
            return redirect('cart_detail', pk=cart_item.cart.pk)
        else:
            messages.error(self.request, "cart not found.")
            return redirect('carts')

    def get_success_url(self):
        if self.object.basket and self.object.basket.pk:
            return reverse_lazy('cart_detail', kwargs={'pk': self.object.basket.pk})
        else:
            return reverse_lazy('carts')
  

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
    template_name = 'c_cart_detail.html'

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
    print("Request method:", request.method)
    print("POST data:", request.POST)
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
        if not cart:
            return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

        product_instance = ProductInstance.objects.filter(cart=cart, product=product).first()

        if product_instance:
            product_instance.amount = amount
            product_instance.save()
        else:
            ProductInstance.objects.create(cart=cart, product=product, amount=amount)

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