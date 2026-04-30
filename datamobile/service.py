from .models import CensoCelular


def get_summary():
    dados = CensoCelular.objects.all()

    total = None
    faixa_lider = None
    maior_valor = 0

    ignorar = {"total", "homens", "mulheres"}

    for item in dados:
        nome = item.grupo_idade.strip().lower()

        # pega a linha Total
        if nome == "total":
            total = item
            continue

        # ignora categorias agregadas
        if nome in ignorar:
            continue

        brasil = item.brasil or 0

        # encontra faixa líder real
        if brasil > maior_valor:
            maior_valor = brasil
            faixa_lider = item.grupo_idade

    if total is None:
        return {"erro": "Linha Total não encontrada"}

    regioes = {
        "Norte": total.norte or 0,
        "Nordeste": total.nordeste or 0,
        "Sudeste": total.sudeste or 0,
        "Sul": total.sul or 0,
        "Centro-Oeste": total.centro_oeste or 0,
    }

    regiao_lider = max(regioes, key=regioes.get)

    return {
        "totalBrasil": total.brasil or 0,
        "regiaoLider": regiao_lider,
        "faixaLider": faixa_lider,
    }

def get_ranking_regioes():
    pass

def get_participacao_percentual():
    pass

def get_heatmap():
    pass

def get_indice_relativo():
    pass

def get_dominante_por_regiao():
    pass

def build_dashboard():
    return {
        "summary": get_summary(),
        "rankingRegioes": get_ranking_regioes(),
        "participacaoPercentual": get_participacao_percentual(),
        "heatmap": get_heatmap(),
        "indiceRelativo": get_indice_relativo(),
        "dominantePorRegiao": get_dominante_por_regiao(),
    }