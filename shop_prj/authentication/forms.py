from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={
        'class':'shadow-lg shadow-stone-250/50 border border-stone-300 appearance-none rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
        'placeholder': 'Email', 'id': 'email'
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'shadow-lg shadow-stone-250/50 border border-stone-300 appearance-none rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
        'placeholder': 'Password','id': 'password',
    }))

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=False, initial=User.CUSTOMER, )# widget=forms.HiddenInput()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'postal_code', 'address')
    
    def __init__(self, *args, user_type=None, **kwargs):
            super().__init__(*args, **kwargs)
            
            if user_type not in ["STAFF", "OWNER"]:
                self.fields['role'].widget = forms.HiddenInput()
                self.fields['role'].initial = User.CUSTOMER


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'shadow-lg shadow-stone-250/50 border border-stone-300 appearance-none rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'New password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'shadow-lg shadow-stone-250/50 border border-stone-300 appearance-none rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Confirm password'
        })
    )

