import math


class IndexedMinMaxHeap:
    """
    Min-Max Heap Indexada para monitoramento de extremos em O(1) e atualização em O(log N).
    - Níveis pares (0, 2, 4...): MÍNIMO (raiz = menor exposição).
    - Níveis ímpares (1, 3, 5...): MÁXIMO (filhos da raiz = maior exposição).
    """

    def __init__(self, num_keys: int = 10000):
        self.n = num_keys
        self.heap = [[0.0, i] for i in range(num_keys)]
        self.pos_map = list(range(num_keys))

    @staticmethod
    def _is_min_level(idx: int) -> bool:
        return ((idx + 1).bit_length() - 1) % 2 == 0

    def _swap(self, i: int, j: int) -> None:
        milhar_i, milhar_j = self.heap[i][1], self.heap[j][1]
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos_map[milhar_i] = j
        self.pos_map[milhar_j] = i

    def peek_min(self) -> tuple[float, int]:
        """Retorna (exposicao, milhar) de menor risco em O(1)."""
        return tuple(self.heap[0])

    def peek_max(self) -> tuple[float, int]:
        """Retorna (exposicao, milhar) de maior risco em O(1)."""
        if self.n == 1:
            return tuple(self.heap[0])
        h1 = self.heap[1]
        if self.n == 2:
            return tuple(h1)
        h2 = self.heap[2]
        return tuple(h1) if h1[0] >= h2[0] else tuple(h2)

    def get_exposure(self, milhar: int) -> float:
        """Consulta a exposição atual de um milhar específico em O(1)."""
        return self.heap[self.pos_map[milhar]][0]

    def update_key(self, milhar: int, delta: float) -> None:
        """Atualiza o valor de exposição de um milhar em O(log N)."""
        idx = self.pos_map[milhar]
        old_val = self.heap[idx][0]
        new_val = old_val + delta
        self.heap[idx][0] = new_val

        if new_val > old_val:
            if self._is_min_level(idx):
                parent = (idx - 1) // 2
                if idx > 0 and new_val > self.heap[parent][0]:
                    self._swap(idx, parent)
                    self._sift_up_max(parent)
                else:
                    self._sift_down_min(idx)
            else:
                self._sift_up_max(idx)
        elif new_val < old_val:
            if not self._is_min_level(idx):
                parent = (idx - 1) // 2
                if idx > 0 and new_val < self.heap[parent][0]:
                    self._swap(idx, parent)
                    self._sift_up_min(parent)
                else:
                    self._sift_down_max(idx)
            else:
                self._sift_up_min(idx)

    def _sift_up_min(self, idx: int) -> None:
        while idx >= 3:
            grandparent = (idx - 3) // 4
            if self.heap[idx][0] < self.heap[grandparent][0]:
                self._swap(idx, grandparent)
                idx = grandparent
            else:
                break

    def _sift_up_max(self, idx: int) -> None:
        while idx >= 3:
            grandparent = (idx - 3) // 4
            if self.heap[idx][0] > self.heap[grandparent][0]:
                self._swap(idx, grandparent)
                idx = grandparent
            else:
                break

    def _sift_down_min(self, idx: int) -> None:
        n = self.n
        heap = self.heap
        while True:
            c1 = 2 * idx + 1
            if c1 >= n:
                break
            min_idx = c1
            min_val = heap[c1][0]
            is_grand = False

            c2 = c1 + 1
            if c2 < n and heap[c2][0] < min_val:
                min_idx = c2
                min_val = heap[c2][0]

            g1 = 2 * c1 + 1
            if g1 < n:
                limit = g1 + 4 if g1 + 4 <= n else n
                for g in range(g1, limit):
                    if heap[g][0] < min_val:
                        min_idx = g
                        min_val = heap[g][0]
                        is_grand = True
            elif c2 < n:
                g3 = 2 * c2 + 1
                if g3 < n:
                    limit = g3 + 2 if g3 + 2 <= n else n
                    for g in range(g3, limit):
                        if heap[g][0] < min_val:
                            min_idx = g
                            min_val = heap[g][0]
                            is_grand = True

            if is_grand:
                if min_val < heap[idx][0]:
                    self._swap(min_idx, idx)
                    parent = (min_idx - 1) // 2
                    if heap[min_idx][0] > heap[parent][0]:
                        self._swap(min_idx, parent)
                    idx = min_idx
                else:
                    break
            else:
                if min_val < heap[idx][0]:
                    self._swap(min_idx, idx)
                break

    def _sift_down_max(self, idx: int) -> None:
        n = self.n
        heap = self.heap
        while True:
            c1 = 2 * idx + 1
            if c1 >= n:
                break
            max_idx = c1
            max_val = heap[c1][0]
            is_grand = False

            c2 = c1 + 1
            if c2 < n and heap[c2][0] > max_val:
                max_idx = c2
                max_val = heap[c2][0]

            g1 = 2 * c1 + 1
            if g1 < n:
                limit = g1 + 4 if g1 + 4 <= n else n
                for g in range(g1, limit):
                    if heap[g][0] > max_val:
                        max_idx = g
                        max_val = heap[g][0]
                        is_grand = True
            elif c2 < n:
                g3 = 2 * c2 + 1
                if g3 < n:
                    limit = g3 + 2 if g3 + 2 <= n else n
                    for g in range(g3, limit):
                        if heap[g][0] > max_val:
                            max_idx = g
                            max_val = heap[g][0]
                            is_grand = True

            if is_grand:
                if max_val > heap[idx][0]:
                    self._swap(max_idx, idx)
                    parent = (max_idx - 1) // 2
                    if heap[max_idx][0] < heap[parent][0]:
                        self._swap(max_idx, parent)
                    idx = max_idx
                else:
                    break
            else:
                if max_val > heap[idx][0]:
                    self._swap(max_idx, idx)
                break