

from .models import categorias
from store.models import  Product


def menu_links(request):
    categoriasfill = categorias.objects.all()
    resultados = []

    for categoria in categoriasfill:
        productos_categoria = Product.objects.filter(categoria_id=categoria.id)
        cantidad_productos = productos_categoria.count()
        resultados.append({'Id': categoria.id,'Categoria': categoria.name, 'Cantidad': cantidad_productos})
 
    return dict(links=resultados)