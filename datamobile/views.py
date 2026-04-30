from django.shortcuts import render

# criar  endpointer
from rest_framework.views import APIView

# resposta json
from rest_framework.response import Response

# importa nosso model que representa a tabela censo_celular
from .models import CensoCelular

from .service import get_summary, get_ranking_regioes, get_heatmap, get_participacao_percentual, get_dominante_por_regiao, get_censo



class CensoCelularView(APIView):
    def get(self, request):
        return Response(get_censo())
    
class SummaryView(APIView):

    def get(self, request):
        return Response(get_summary())
    
class RankingRegioesView(APIView):
    def get(self, request):
        return Response(get_ranking_regioes())
    
class HeatmapView(APIView):
    def get(self, request):
        return Response(get_heatmap())
    
class ParticipacaoPercentualView(APIView):
    def get(self, request):
        return Response(get_participacao_percentual())
    
class DominanteRegiao(APIView):
    def get(self, request):
        return Response(get_dominante_por_regiao())

    
    