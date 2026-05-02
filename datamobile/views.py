from django.shortcuts import render


from rest_framework.views import APIView

from rest_framework.response import Response

from .service import *


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
    
class DominanteRegiaoView(APIView):
    def get(self, request):
        return Response(get_dominante_por_regiao())
    
class DashboardBuildView(APIView):
    def get(self, request):
        return Response(build_dashboard())

    
    