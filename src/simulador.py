import random
import statistics
import time
from src.modelos import BancaMitigadaMinMax, BancaTradicional


def gerar_fluxo_apostas(
    qtd_apostas: int = 100000, seed: int = 42
) -> list[tuple[int, float, bool]]:
    """
    Gera carga sintética realista: 70% uniforme e 30% concentrada em
    15 milhares populares (efeito manada: datas, sonhos, placas).
    """
    rng = random.Random(seed)
    numeros_populares = [rng.randint(0, 9999) for _ in range(15)]
    fluxo = []
    for _ in range(qtd_apostas):
        is_surpresinha = rng.random() < 0.15
        milhar = (
            rng.choice(numeros_populares)
            if rng.random() < 0.30
            else rng.randint(0, 9999)
        )
        valor = rng.choice([2.0, 5.0, 10.0, 20.0, 50.0])
        fluxo.append((milhar, valor, is_surpresinha))
    return fluxo


def rodar_benchmark_tempo(
    qtd_apostas: int = 100000, intervalo_inspecao: int = 100
) -> dict:
    """Métrica 1: Compara tempo de monitoramento O(N) vs O(1)."""
    fluxo = gerar_fluxo_apostas(qtd_apostas=qtd_apostas, seed=99)

    banca_trad = BancaTradicional()
    t0 = time.perf_counter()
    for i, (m, v, _) in enumerate(fluxo):
        banca_trad.registrar_aposta(m, v)
        if i % intervalo_inspecao == 0:
            banca_trad.consultar_extremos()
    tempo_trad_ms = (time.perf_counter() - t0) * 1000

    banca_heap = BancaMitigadaMinMax()
    t0 = time.perf_counter()
    for i, (m, v, surp) in enumerate(fluxo):
        banca_heap.registrar_aposta(m, v, surp)
        if i % intervalo_inspecao == 0:
            _ = banca_heap.heap.peek_min(), banca_heap.heap.peek_max()
    tempo_heap_ms = (time.perf_counter() - t0) * 1000

    return {
        "qtd_apostas": qtd_apostas,
        "qtd_inspecoes": qtd_apostas // intervalo_inspecao,
        "tempo_trad_ms": tempo_trad_ms,
        "tempo_heap_ms": tempo_heap_ms,
        "speedup": tempo_trad_ms / tempo_heap_ms,
    }


def rodar_monte_carlo(
    num_simulacoes: int = 1000, apostas_por_dia: int = 50000
) -> dict:
    """Métricas 2 e 3: Avalia taxa de falência, balanço financeiro e decisões."""
    falencias_trad, falencias_heap = 0, 0
    saldos_trad, saldos_heap = [], []
    soma_decisoes = {
        "descarregos": 0,
        "valor_descarregado_total": 0.0,
        "travamentos": 0,
        "surpresinhas": 0,
        "odds_reduzidas": 0,
        "odds_bonificadas": 0,
    }

    for sim in range(num_simulacoes):
        fluxo = gerar_fluxo_apostas(qtd_apostas=apostas_por_dia, seed=sim)
        sorteado = random.Random(sim + 10000).randint(0, 9999)

        bt = BancaTradicional(caixa_inicial=100000.0)
        bh = BancaMitigadaMinMax(
            caixa_inicial=100000.0,
            teto_descarrego=80000.0,
            teto_hard_cap=120000.0,
        )

        for m, v, surp in fluxo:
            bt.registrar_aposta(m, v)
            bh.registrar_aposta(m, v, surp)

        saldo_t, faliu_t = bt.apurar_sorteio(sorteado)
        saldo_h, faliu_h = bh.apurar_sorteio(sorteado)

        falencias_trad += int(faliu_t)
        falencias_heap += int(faliu_h)
        saldos_trad.append(saldo_t)
        saldos_heap.append(saldo_h)

        for k in soma_decisoes:
            soma_decisoes[k] += bh.decisoes[k]

    media_decisoes = {k: v / num_simulacoes for k, v in soma_decisoes.items()}

    return {
        "num_simulacoes": num_simulacoes,
        "apostas_por_dia": apostas_por_dia,
        "falencias_trad": falencias_trad,
        "falencias_heap": falencias_heap,
        "media_trad": statistics.mean(saldos_trad),
        "mediana_trad": statistics.median(saldos_trad),
        "pior_trad": min(saldos_trad),
        "melhor_trad": max(saldos_trad),
        "media_heap": statistics.mean(saldos_heap),
        "mediana_heap": statistics.median(saldos_heap),
        "pior_heap": min(saldos_heap),
        "melhor_heap": max(saldos_heap),
        "media_decisoes": media_decisoes,
    }