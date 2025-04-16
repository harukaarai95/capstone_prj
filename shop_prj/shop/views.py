# from django.shortcuts import render

# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin
from .decorators import role_required
from django.shortcuts import render, redirect
from django.views import generic
from authentication.models import User
from .models import Product

def home(request):
    return render(request, 'index.html')

@login_required
@role_required(allowed_roles=['STAFF', 'MASTER'])
def staff_home(request):
    return render(request, 'staff.html')


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