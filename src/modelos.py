from src.heap import IndexedMinMaxHeap


class BancaTradicional:
    """Modelo Reativo: armazena apostas em vetor linear e usa varredura O(N)."""

    def __init__(self, caixa_inicial: float = 100000.0):
        self.caixa = caixa_inicial
        self.apostas = [0.0] * 10000
        self.cotacao_fixa = 4000.0

    def registrar_aposta(self, milhar: int, valor: float) -> bool:
        self.apostas[milhar] += valor
        self.caixa += valor
        return True

    def consultar_extremos(self) -> tuple[tuple[float, int], tuple[float, int]]:
        """Varredura sequencial O(N) para identificar maior e menor exposição."""
        min_val, min_m = float("inf"), -1
        max_val, max_m = float("-inf"), -1
        for m in range(10000):
            v = self.apostas[m]
            if v < min_val:
                min_val, min_m = v, m
            if v > max_val:
                max_val, max_m = v, m
        return (min_val, min_m), (max_val, max_m)

    def apurar_sorteio(self, milhar_sorteado: int) -> tuple[float, bool]:
        premio = self.apostas[milhar_sorteado] * self.cotacao_fixa
        self.caixa -= premio
        return self.caixa, self.caixa < 0


class BancaMitigadaMinMax:
    """Modelo Proativo: usa Min-Max Heap em O(1)/O(log N) para aplicar as 4 defesas."""

    def __init__(
        self,
        caixa_inicial: float = 100000.0,
        teto_descarrego: float = 80000.0,
        teto_hard_cap: float = 120000.0,
    ):
        self.caixa = caixa_inicial
        self.heap = IndexedMinMaxHeap(10000)
        self.passivo_potencial = [0.0] * 10000
        self.teto_descarrego = teto_descarrego
        self.teto_hard_cap = teto_hard_cap

        # Auditoria das tomadas de decisão em tempo real
        self.decisoes = {
            "descarregos": 0,
            "valor_descarregado_total": 0.0,
            "travamentos": 0,
            "surpresinhas": 0,
            "odds_reduzidas": 0,
            "odds_bonificadas": 0,
        }

    def _calcular_odd_dinamica(self, milhar: int) -> float:
        """Estratégia 4: Cotas Dinâmicas baseadas na posição relativa aos extremos."""
        min_exp, _ = self.heap.peek_min()
        max_exp, _ = self.heap.peek_max()
        atual_exp = self.heap.get_exposure(milhar)

        if max_exp == min_exp:
            return 4000.0

        ratio = (atual_exp - min_exp) / (max_exp - min_exp)
        if ratio > 0.75:
            self.decisoes["odds_reduzidas"] += 1
            return 3200.0  # Desestimula números sobrecarregados
        if ratio < 0.15:
            self.decisoes["odds_bonificadas"] += 1
            return 4300.0  # Bônus para números frios (raiz de mínimo)
        return 4000.0

    def registrar_aposta(
        self, milhar: int, valor: float, is_surpresinha: bool = False
    ) -> bool:
        # Estratégia 3: Surpresinha Inteligente direciona para a raiz de mínimo em O(1)
        if is_surpresinha:
            _, milhar = self.heap.peek_min()
            self.decisoes["surpresinhas"] += 1

        exposicao_atual = self.heap.get_exposure(milhar)
        odd = self._calcular_odd_dinamica(milhar)
        novo_passivo = exposicao_atual + (valor * odd)

        # Estratégia 2: Travamento (Hard Cap / Circuit Breaker)
        if novo_passivo > self.teto_hard_cap:
            self.decisoes["travamentos"] += 1
            return False

        # Estratégia 1: Descarrego (Repasse do excedente para banca parceira)
        valor_retido = valor
        if novo_passivo > self.teto_descarrego:
            excedente_passivo = novo_passivo - self.teto_descarrego
            valor_descarregado = excedente_passivo / odd
            valor_retido = max(0.0, valor - valor_descarregado)
            self.decisoes["descarregos"] += 1
            self.decisoes["valor_descarregado_total"] += (
                valor - valor_retido
            )

        passivo_retido = valor_retido * odd
        self.caixa += valor_retido
        self.passivo_potencial[milhar] += passivo_retido
        self.heap.update_key(milhar, passivo_retido)
        return True

    def apurar_sorteio(self, milhar_sorteado: int) -> tuple[float, bool]:
        premio = self.passivo_potencial[milhar_sorteado]
        self.caixa -= premio
        return self.caixa, self.caixa < 0