

from .models import Departamento
from store.models import  Product


def menu_links(request):
    Departamentofill = Departamento.objects.all()
    resultados = []

    # for categoria in Departamentofill:
    #     productos_categoria = Product.objects.filter(categoria_id=categoria.id)
    #     cantidad_productos = productos_categoria.count()
    #     resultados.append({'Id': categoria.id,'Categoria': categoria.name, 'Cantidad': cantidad_productos})
 
    return dict(links=Departamentofill)