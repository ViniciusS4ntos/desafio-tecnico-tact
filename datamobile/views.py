from django.shortcuts import render

# criar  endpointer
from rest_framework.views import APIView

# resposta json
from rest_framework.response import Response

# importa nosso model que representa a tabela censo_celular
from .models import CensoCelular

from .service import get_summary



class CensoCelularView(APIView):
    def get(self, request):
        # Buscar no banco todos os dados
        dados = CensoCelular.objects.all().values()

        # retorna os dados
        return Response({
            "total_registros" : dados.count(),
            "dados": list(dados)
        })
    
class SummaryView(APIView):

    def get(self, request):
        return Response(get_summary())

    
    