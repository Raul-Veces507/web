from django.db import models
from store.models import Product
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.


class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)  # Campo para la fecha de vencimiento

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            current_date = datetime.now()
            # Si no se ha establecido la fecha de vencimiento, establece 5 días después de la creación
            self.expiry_date = current_date + timedelta(days=5)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def subtotal(self):
        return self.product.precio*self.quantity


    def __unicode__(self):
        return self.product


@receiver(pre_delete, sender=Cart)
def delete_expired_carts(sender, instance, **kwargs):
    # Eliminar carritos vencidos antes de su eliminación
    Cart.objects.filter(expiry_date__lt=timezone.now()).delete()
    
