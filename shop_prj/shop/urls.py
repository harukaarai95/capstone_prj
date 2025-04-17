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
    path('staff/product/add/', views.CreateProductView.as_view(), name='product_add'),
    path('staff/product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('staff/product/<int:pk>/edit/', views.edit_product, name='product_edit'),
    path('staff/product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('staff/genre/add/', views.CreateGenreView.as_view(), name='genre_add'),
    path('staff/genres/', views.GenreListView.as_view(), name='genres'),
    path('staff/genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('staff/genre/<int:pk>/edit/', views.EditGenreView.as_view(), name='genre_edit'),
    path('staff/genre/<int:pk>/delete/', views.DeleteGenreView.as_view(), name='genre_delete'),


]