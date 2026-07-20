from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.stock_view, name='stock'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:item_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:item_id>/', views.delete_item, name='delete_item'),
]