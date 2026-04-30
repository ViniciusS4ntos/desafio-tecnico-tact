from .models import CensoCelular

def get_censo():
        # Buscar no banco todos os dados
        dados = CensoCelular.objects.all().values()

        # retorna os dados
        return ({
            "total_registros" : dados.count(),
            "dados": list(dados)
        })

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
    dados = CensoCelular.objects.all()

    total = None

    # achar linha Total
    for item in dados:
        nome = item.grupo_idade.strip().lower()

        if nome == "total":
            total = item
            break

    if total is None:
        return []
    
    total_brasil = total.brasil or 0

    if total_brasil == 0:
        return []
        
    regioes = [
    ("Norte", total.norte or 0),
    ("Nordeste", total.nordeste or 0),
    ("Sudeste", total.sudeste or 0),
    ("Sul", total.sul or 0),
    ("Centro-Oeste", total.centro_oeste or 0),
    ]

    participacao = []

    for nome_regiao, valor in regioes:
        percentual = round((valor / total_brasil) * 100, 2)

        participacao.append({
            "regiao": nome_regiao,
            "percentual": percentual
        })

    participacao.sort(
        key=lambda item: item["percentual"],
        reverse=True
    )

    return participacao

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

def get_dominante_por_regiao(): 
    dados = CensoCelular.objects.all()

    capturando = False
    faixas = []

    # pega somente faixa geral
    for item in dados:
        nome = item.grupo_idade.strip().lower()

        if nome == "total":
            capturando = True
            continue

        if nome == "homens":
            break

        if capturando:
            faixas.append(item)

    if not faixas:
        return []

    regioes = {
        "Norte": ("", 0),
        "Nordeste": ("", 0),
        "Sudeste": ("", 0),
        "Sul": ("", 0),
        "Centro-Oeste": ("", 0),
    }

    for item in faixas:
        valores = {
            "Norte": item.norte or 0,
            "Nordeste": item.nordeste or 0,
            "Sudeste": item.sudeste or 0,
            "Sul": item.sul or 0,
            "Centro-Oeste": item.centro_oeste or 0,
        }

        for regiao, valor in valores.items():
            maior_atual = regioes[regiao][1]

            if valor > maior_atual:
                regioes[regiao] = (
                    item.grupo_idade,
                    valor
                )

    resultado = []

    for regiao, info in regioes.items():
        resultado.append({
            "regiao": regiao,
            "faixaDominante": info[0],
            "totalPosses" : info[1]
        })

    return resultado

def build_dashboard(): 
    return {
        "summary": get_summary(),
        "rankingRegioes": get_ranking_regioes(),
        "participacaoPercentual": get_participacao_percentual(),
        "heatmap": get_heatmap(),
        "dominantePorRegiao": get_dominante_por_regiao(),
    }