from django.urls import path
from . import views

urlpatterns=[
    path('', views.store,name="store"),
    path('category/<int:category_slug>/',views.store,name='products_by_category'),
    path('category/<str:category_slug>/<str:Marca_slug>/',views.products_by_category_marca,name='products_by_category_marca'),
    path('product/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
]