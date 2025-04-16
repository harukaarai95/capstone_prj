from django.urls import path
from . import views
import authentication.views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', authentication.views.login_view, name='login'),
    path('logout/', authentication.views.logout_view, name='logout'),
    path('signup/', authentication.views.signup_view, name='signup'),
    path('staff/', views.staff_home, name='staff_home'),
    path('staff/products/', views.ProductListView.as_view(), name='products'),
    path('staff/product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),


]