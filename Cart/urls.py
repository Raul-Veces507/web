from django.urls import path
from . import views

urlpatterns=[
    path('', views.cart,name="cart"),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('viewfiltcart/', views.viewfiltcart, name='viewfiltcart'),
    path('add_cart/<int:product_id>', views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>', views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>', views.remove_cart_item,name="remove_cart_item"),
    path('checkout/',views.checkout, name='checkout')
]