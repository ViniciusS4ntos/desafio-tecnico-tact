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
    dados = CensoCelular.objects.all()

    total = None

    for item in dados:
        nome = item.grupo_idade.strip().lower()

        if nome == "total":
            total = item
            break

    if total is None:
        return []

    ranking = [
        {"regiao": "Norte", "total": total.norte or 0},
        {"regiao": "Nordeste", "total": total.nordeste or 0},
        {"regiao": "Sudeste", "total": total.sudeste or 0},
        {"regiao": "Sul", "total": total.sul or 0},
        {"regiao": "Centro-Oeste", "total": total.centro_oeste or 0},
    ]

    ranking.sort(
        key=lambda item: item["total"],
        reverse=True
    )

    return ranking

def get_participacao_percentual():
    pass

def get_heatmap():
    dados = CensoCelular.objects.all()

    heatmap = []
    capturando = False

    for item in dados:
        nome = item.grupo_idade.strip().lower()

        # começa após Total
        if nome == "total":
            capturando = True
            continue

        # parou quando chegou em Homens
        if nome == "homens":
            break

        # só captura faixa etária geral
        if capturando:
            heatmap.append({
                "faixaEtaria": item.grupo_idade,
                "norte": item.norte or 0,
                "nordeste": item.nordeste or 0,
                "sudeste": item.sudeste or 0,
                "sul": item.sul or 0,
                "centroOeste": item.centro_oeste or 0,
            })

    return heatmap

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