def get_summary():
    pass

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