from django.urls import path
from . import views

urlpatterns=[
    path('', views.store,name="store"),
    path('category/<int:category_slug>/',views.store,name='products_by_category'),
]