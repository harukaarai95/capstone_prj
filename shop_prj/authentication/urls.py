# authentication/urls.py

from django.urls import path
from . import views
from .views import CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('customer/<int:pk>/', views.CustomerUserDetailView.as_view(), name='c_user_detail'),
    path('customer/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='c_user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
