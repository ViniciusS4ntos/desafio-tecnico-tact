# importa path para criar rota
from django.urls import path

# importa nossa view
from .views import CensoCelularView

from .views import SummaryView

from .views import RankingRegioesView

from .views import HeatmapView


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

    path(
        "ranking/",
        RankingRegioesView.as_view()
    ),

    path(
        "heatmap/",
        HeatmapView.as_view()
    )
]