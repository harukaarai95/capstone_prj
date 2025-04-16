# from django.shortcuts import render

# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import role_required
from django.shortcuts import render, redirect
from django.views import generic
from authentication.models import User


def home(request):
    return render(request, 'index.html')

@login_required
@role_required(allowed_roles=['STAFF', 'OWNER'])
def staff_home(request):
    return render(request, 'staff.html')

class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user_list.html'