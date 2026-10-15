"""Regras de nível e desconto (antes em scriptPerfil.js / scriptCarrinho.js)."""


def calcular_desconto(qtd_viagens):
    return calcular_nivel(qtd_viagens)["desconto"]


def calcular_nivel(qtd):
    if qtd >= 10:
        return {"nivel": "Diamante", "desconto": 20, "proximo": "Máximo", "progresso": 100,
                "texto": "Parabéns! Você chegou ao nível máximo e desbloqueou 20% de desconto."}
    for minimo, nome, desconto, proximo, maximo in [
        (6, "Ouro", 15, "Diamante", 10),
        (3, "Prata", 10, "Ouro", 6),
        (0, "Bronze", 5, "Prata", 3),
    ]:
        if qtd >= minimo:
            progresso = round((qtd - minimo) / (maximo - minimo) * 100)
            return {"nivel": nome, "desconto": desconto, "proximo": proximo,
                    "progresso": max(0, min(100, progresso)),
                    "texto": f"Faltam {maximo - qtd} viagem(ns) para chegar ao nível {proximo}."}
