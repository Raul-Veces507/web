from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.





class adminCartItem(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')


admin.site.register(CartItem,adminCartItem)

admin.site.register(Cart)