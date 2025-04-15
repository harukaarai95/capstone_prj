from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()
    first_name = models.CharField(max_length=250, verbose_name='first name')
    last_name = models.CharField(max_length=250, verbose_name='last name')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email' # use email to login
    MASTER = 'MASTER'
    STAFF = 'STAFF'
    CUSTOMER = 'CUSTOMER'
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)

    ROLE_CHOICES = (
        (MASTER, 'MASTER'),
        (STAFF, 'STAFF'),
        (CUSTOMER, 'CUSTOMER'),
        )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="CUSTOMER")
    joined_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-joined_on']
    
    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.id}: {self.last_name} {self.first_name}"
