from django.contrib import admin
from .models import categorias
# Register your models here.

class admincategorias(admin.ModelAdmin):
    list_display=('name','departamento','created_at','updated_at')
    search_fields=['name','departamento']


admin.site.register(categorias,admincategorias)
