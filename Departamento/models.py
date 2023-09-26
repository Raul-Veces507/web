
from django.db import models
from django.urls import reverse
# Create your models here.
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    

    def get_url(self):
        return reverse('products_by_departamento',args=[self.id])
    