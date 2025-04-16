from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from authentication.models import User
from . import forms
from .forms import CustomSetPasswordForm
from shop.mixins import RoleRequiredMixin

def login_view(request):
    message = ""
    form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None and user.role != 'CUSTOMER':
                login(request, user)
                message = _("Login success!")
                return redirect('staff_home')
            elif user is not None and user.role == 'CUSTOMER':
                login(request, user)
                message = _("Login success!")
                return redirect('home')
            else:
                message = _("Login Failed")

    return render(
        request, 'registration/login.html', context={'form': form, 'message': message}
    )

@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def signup_view(request):
    user_type = request.user.role if request.user.is_authenticated else None
    form = forms.SignupForm(user_type=user_type)

    if request.method == 'POST':
        form = forms.SignupForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(commit=False)
            if not request.user.is_authenticated or request.user.role not in ["STAFF", "OWNER"]:
                user.role = "CUSTOMER"  # set as customer
            user.save()
            return redirect('home')
    
    return render(request, 'registration/signup.html', context={'form': form})

class UserListView(LoginRequiredMixin, RoleRequiredMixin, generic.ListView):
    allowed_roles = ['STAFF', 'MASTER']
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'

class UserDetailView(LoginRequiredMixin, RoleRequiredMixin, generic.DetailView):
    allowed_roles = ['STAFF', 'MASTER']
    model = User
    template_name = 'authentication/user_detail.html'
    context_object_name = 'user_detail'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'authentication/user_edit.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'postal_code', 'address', 'role']
    success_url = reverse_lazy('user_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.role != User.MASTER:
            form.fields.pop('role')
        return form

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user.role == User.CUSTOMER and request.user.pk != obj.pk:
            raise PermissionDenied(_("You can only edit your own information."))

        if request.user.role in [User.MASTER, User.STAFF] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied(_("You do not have permission to access this page."))

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm