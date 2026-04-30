# importa path para criar rota
from django.urls import path

# importa nossa view
from .views import CensoCelularView

from .views import SummaryView


# lista de rotas da app
urlpatterns = [

    path(
        "censo/",
        CensoCelularView.as_view(),
        name="censo-celular"
        ),

    path(
        "summary/", 
        SummaryView.as_view()
        ),
]