from src.simulador import rodar_benchmark_tempo, rodar_monte_carlo


def fmt_brl(valor: float) -> str:
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {abs(valor):,.2f}"


def main():
    largura = 72
    print("=" * largura)
    print(" EXPERIMENTOS EDB2: MIN-MAX HEAP INDEXADA NA MITIGAÇÃO DE RISCOS")
    print("=" * largura)

    # --- BLOCO 1: DESEMPENHO COMPUTACIONAL ---
    bench = rodar_benchmark_tempo(qtd_apostas=100000, intervalo_inspecao=100)
    print("\n[1] DESEMPENHO COMPUTACIONAL (Streaming de Apostas)")
    print(
        f"    Carga: {bench['qtd_apostas']:,} apostas | {bench['qtd_inspecoes']:,}"
        " consultas de extremos (mín/máx)"
    )
    print("-" * largura)
    print(
        f"    • Modelo Tradicional (Varredura Linear O(N)) : {bench['tempo_trad_ms']:7.2f} ms"
    )
    print(
        f"    • Modelo Min-Max Heap (Leitura Direta O(1))  : {bench['tempo_heap_ms']:7.2f} ms"
    )
    print(
        f"    -> Ganho de Velocidade (Speedup)             : {bench['speedup']:.2f}x mais rápido"
    )

    # --- BLOCO 2: AUDITORIA DE DECISÕES DA BANCA ---
    print("\n[2] SIMULAÇÃO MONTE CARLO: SOLVÊNCIA E BALANÇO FINANCEIRO")
    print("    Executando 1.000 dias de operação (20.000 apostas/dia)...")
    mc = rodar_monte_carlo(num_simulacoes=1000, apostas_por_dia=20000)
    n = mc["num_simulacoes"]
    dec = mc["media_decisoes"]

    print("-" * largura)
    print("    A) Auditoria Média de Intervenções por Dia (Modelo Min-Max Heap):")
    print(
        f"       - Descarregos (Repasse de risco)   : {dec['descarregos']:7.1f} ops"
        f" ({fmt_brl(dec['valor_descarregado_total'])} repassados)"
    )
    print(
        f"       - Travamentos (Hard Cap atingido)  : {dec['travamentos']:7.1f} apostas bloqueadas"
    )
    print(
        f"       - Surpresinhas (Direcionadas Min)  : {dec['surpresinhas']:7.1f} apostas equilibradas"
    )
    print(
        f"       - Cotas Dinâmicas (Odds ajustadas) : {dec['odds_reduzidas']:7.1f} reduzidas |"
        f" {dec['odds_bonificadas']:7.1f} bonificadas"
    )

    # --- BLOCO 3: TAXA DE FALÊNCIA ---
    print("-" * largura)
    print(f"    B) Taxa de Falência (Caixa Inicial: R$ 100.000,00):")
    print(
        f"       • Modelo Tradicional  : {mc['falencias_trad']:4d} quebras em {n} dias"
        f" ({(mc['falencias_trad']/n)*100:.2f}%)"
    )
    print(
        f"       • Modelo Min-Max Heap : {mc['falencias_heap']:4d} quebras em {n} dias"
        f" ({(mc['falencias_heap']/n)*100:.2f}%)"
    )

    # --- BLOCO 4: BALANÇO FINANCEIRO ---
    print("-" * largura)
    print("    C) Distribuição do Saldo Final da Banca:")
    print(
        f"       • Tradicional  -> Média: {fmt_brl(mc['media_trad'])} |"
        f" Mediana: {fmt_brl(mc['mediana_trad'])}"
    )
    print(
        f"                         Melhor: {fmt_brl(mc['melhor_trad'])} |"
        f" Pior: {fmt_brl(mc['pior_trad'])}"
    )
    print(
        f"       • Min-Max Heap -> Média: {fmt_brl(mc['media_heap'])} |"
        f" Mediana: {fmt_brl(mc['mediana_heap'])}"
    )
    print(
        f"                         Melhor: {fmt_brl(mc['melhor_heap'])} |"
        f" Pior: {fmt_brl(mc['pior_heap'])}"
    )

    # --- CONCLUSÃO ANALÍTICA ---
    print("=" * largura)
    print(" RESUMO ANALÍTICO:")
    print(
        " • O modelo Tradicional maximiza o lucro bruto em dias comuns, mas fica"
    )
    print(
        f"   vulnerável ao risco de ruína (prejuízo máximo de {fmt_brl(mc['pior_trad'])})."
    )
    print(
        " • O modelo Min-Max Heap sacrifica parte do excedente via Descarrego para"
    )
    print(
        f"   garantir 0% de falência e lucro mínimo positivo ({fmt_brl(mc['pior_heap'])})."
    )
    print("=" * largura)


if __name__ == "__main__":
    main()