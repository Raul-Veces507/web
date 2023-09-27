from django.urls import path
from . import views

urlpatterns=[
    path('', views.store,name="store"),
    path('Departamento/<int:category_slug>/',views.store,name='products_by_departamento'),
    path('category/<int:category_slug>/',views.products_by_category,name='products_by_category'),
    path('category/<str:category_slug>/<path:Marca_slug>/',views.products_by_category_marca,name='products_by_category_marca'),
    path('product/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
]