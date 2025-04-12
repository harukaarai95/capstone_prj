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

def login_page(request):
    message = ""
    form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = _("Login success!")
                print("Authenticated user:", request.user)
                print("Is authenticated:", request.user.is_authenticated)
                return redirect('index')
            else:
                message = _("Login Failed")

    return render(
        request, 'registration/login.html', context={'form': form, 'message': message}
    )

@login_required
def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def signup_page(request):
    user_type = request.user.role if request.user.is_authenticated else None
    form = forms.SignupForm(user_type=user_type)

    if request.method == 'POST':
        form = forms.SignupForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(commit=False)
            if not request.user.is_authenticated or request.user.role not in ["STAFF", "OWNER"]:
                user.role = "CUSTOMER"  # set as customer
            user.save()
            return redirect('index')
    
    return render(request, 'registration/signup.html', context={'form': form})

# for admin user
class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == User.CUSTOMER:
            messages.error(request, _("You do not have permission to access this page."))
            return redirect(reverse_lazy('index'))
        return super().dispatch(request, *args, **kwargs)

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'authentication/user_detail.html'
    context_object_name = 'user_detail'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'authentication/user_edit.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'postal_code', 'address', 'role']
    success_url = reverse_lazy('users')
    def get_form(self, *args, **kwargs):# drop role if the logged in user is customer
        form = super().get_form(*args, **kwargs)
        if self.request.user.role == User.CUSTOMER:
            form.fields.pop('role')
        return form
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user.role == User.CUSTOMER and request.user.pk != obj.pk:
            raise PermissionDenied(_("You can only edit your own information."))
        
        if request.user.role == User.MASTER or User.STAFF or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied(_("You do not have permission to access this page."))

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm