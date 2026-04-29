# importa path para criar rota
from django.urls import path

# importa nossa view
from .views import CensoCelularView


# lista de rotas da app
urlpatterns = [

    # rota:
    # /api/censo/
    #
    # quando alguém acessar:
    # chama CensoCelularView
    path(
        "censo/",
        CensoCelularView.as_view(),
        name="censo-celular"
    ),
]