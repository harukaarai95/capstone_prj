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

def home(request):
    return render(request, 'index.html')

@login_required
@role_required(allowed_roles=['STAFF', 'MASTER'])
def staff_home(request):
    return render(request, 'staff.html')


class UserListView(LoginRequiredMixin, RoleRequiredMixin, generic.ListView):
    allowed_roles = ['STAFF', 'MASTER']
    model = User
    context_object_name = 'users'
    template_name = 'user_list.html'

class UserDetailView(LoginRequiredMixin, RoleRequiredMixin, generic.DetailView):
    allowed_roles = ['STAFF', 'MASTER']
    model = User
    context_object_name = 'user_detail'
    template_name = 'user_detail_for_staff.html'