from django.urls import path
from . import views
import authentication.views
from .views import CustomerCartDetail

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
    path('goods/', views.CustomerProductListView.as_view(), name='customer_goods'),
    path('goods/<int:pk>/', views.CustomerProductDetailView.as_view(), name='customer_goods_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('user/cart/', CustomerCartDetail.as_view(), name='c_cart_detail'),
    path('remove_item/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('purchase/<int:product_id>/', views.purchase_item, name='purchase_item'),
    path('purchase_all/', views.purchase_all, name='purchase_all'),
    path('order_history/',views.PurchaseHistoryView.as_view(), name='order_history'),

]