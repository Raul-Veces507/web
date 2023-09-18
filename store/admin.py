from django.contrib import admin
from .models import Product,Banner,ProductViewBanner,ProductViewPrincipal
from django.utils.html import format_html
# Register your models here.


class adminProduct(admin.ModelAdmin):
    list_display=('nombre','item','sku','inventario','bodega','Marca','events_id','categoria_id','subcategoria_id')
    search_fields=['nombre','item','sku','bodega','Marca']

class adminBanner(admin.ModelAdmin):
       def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.images.url))
       thumbnail.short_description="imagen de perfil"
       list_display=('thumbnail','nombre','fechainicial','fechaFinal','created_date')

class adminProductViewBanner(admin.ModelAdmin):
       def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.images.url))
       thumbnail.short_description="imagen de perfil"
       list_display=('thumbnail','Banner','product')

class adminProductViewPrincipal(admin.ModelAdmin):

       list_display=('product','status','created_at','update_at')



admin.site.register(Banner,adminBanner)

admin.site.register(Product,adminProduct)

admin.site.register(ProductViewBanner)

admin.site.register(ProductViewPrincipal)
