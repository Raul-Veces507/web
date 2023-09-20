

from .models import categorias


def menu_links(request):
    links=categorias.objects.all()
    return dict(links=links)