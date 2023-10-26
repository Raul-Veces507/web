from django.urls import path
from . import views

urlpatterns=[
    path('', views.store,name="store"),
    path('Departamento/<int:depar>/',views.store,name='products_by_departamento'),
    path('obtenerinfoproduct/',views.obtenerinfoproduct,name='obtenerinfoproduct'),
    path('search/',views.search,name='search'),
    path('searchC/',views.searchfillCategoria,name='searchfillCategoria'),
    path('searchM/', views.searchfillmarca, name='searchfillmarca'),

    
    path('category/<int:category_slug>/',views.products_by_category,name='products_by_category'),
    path('category/<str:category_slug>/<path:Marca_slug>/',views.products_by_category_marca,name='products_by_category_marca'),
    path('product/<int:product>/',views.product_detail,name='product_detail'),
    path('Seccion/<str:seccion>/',views.Seccion,name='Seccion'),
    path('Seccion/<str:seccion>/<int:categoria>/',views.SeccionfillCategoria,name='SeccionfillCategoria'),
    path('Seccion/<str:seccion>/<str:marca>/', views.Seccionfillmarca, name='Seccionfillmarca'),

    path('upload_excel/', views.upload_excel, name='upload_excel'),

         
]