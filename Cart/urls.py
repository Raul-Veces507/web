from django.urls import path
from . import views

urlpatterns=[
    path('', views.cart,name="cart"),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('viewfiltcart/', views.viewfiltcart, name='viewfiltcart'),
    path('add_cart_comentatario/', views.add_cart_comentatario,name="add_cart_comentatario"),
    path('addComentario/', views.addComentario,name="addComentario"),
    
    path('ValidarCarrito/', views.ValidarCarrito,name="ValidarCarrito"),
    path('add_cart/<int:product_id>', views.add_cart,name="add_cart"),
    path('add_cart_detail/', views.add_cart_detail,name="add_cart_detail"),
    path('remove_cart/<int:product_id>', views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>', views.remove_cart_item,name="remove_cart_item"),
    path('EliminarCarrtioCompleto/', views.EliminarCarrtioCompleto,name="EliminarCarrtioCompleto"),
    path('checkout/',views.checkout, name='checkout'),
    path('completeorder/<str:Orden>/', views.completarorden, name="completeorder"),

    
]

