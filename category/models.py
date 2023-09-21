from django.urls import reverse
from django.db import models

# Create your models here.
class categorias(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'categorias'  # Especifica el nombre de la tabla existente en la base de datos
    def __str__(self):
        return self.name
    

    def get_url(self):
        return reverse('products_by_category',args=[self.id])
    

    
  