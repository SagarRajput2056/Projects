from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.account_detail, name='account_detail'),
    path('my-store/', views.my_store, name='my_store'),
    path('toggle_order_status/<int:order_id>/', views.toggle_order_status, name='toggle_order_status'),
    path('my-store/order-detail/<int:pk>/', views.store_order_detail, name='store_order_detail'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]