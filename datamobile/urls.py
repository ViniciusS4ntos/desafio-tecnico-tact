# importa path para criar rota
from django.urls import path

# importa nossa view
from .views import CensoCelularView

from .views import SummaryView

from .views import RankingRegioesView

from .views import HeatmapView

from .views import ParticipacaoPercentualView

from .views import DominanteRegiaoView

from .views import DashboardBuildView


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
    ),

    path(
        "participacao/",
        ParticipacaoPercentualView.as_view()
    ),

    path(
        "dominante-regiao/",
        DominanteRegiaoView.as_view()
        ),

    path("dashboard/",
         DashboardBuildView.as_view()
         )

]