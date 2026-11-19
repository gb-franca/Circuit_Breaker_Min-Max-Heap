# 🎰 Mitigação de Risco em Apostas com Min-Max Heap Indexada

Projeto desenvolvido para a disciplina de **Estruturas de Dados Básicas II (EDB2)**. O objetivo é demonstrar a aplicação prática de uma **Min-Max Heap Indexada** em tempo real para controle de exposição de risco financeiro, prevenção de ruína (falência) e mitigação do "efeito manada" em sistemas de apostas de quota fixa (e.g., milhares de 0000 a 9999).

---

## 📌 Contexto e Motivação

Em mercados de apostas e loterias, a distribuição de apostas nunca é perfeitamente uniforme. Usuários tendem a concentrar capital em datas comemorativas, finais de placas de carro ou números de sorte (**efeito manada**). 

* **No Modelo Tradicional (Reativo):** As bancas operam com cotas fixas (ex: 4.000x) e armazenam os dados em vetores lineares simples. Identificar quais números representam maior ou menor passivo exige varreduras lineares $\mathcal{O}(N)$. Em dias de grande concentração, se o número mais apostado for sorteado, a banca enfrenta um passivo astronômico que pode superar o capital disponível em dezenas de vezes, culminando na **falência imediata**.
* **No Modelo Mitigado (Proativo):** Utiliza-se uma **Min-Max Heap Indexada** capaz de consultar o milhar mais perigoso (máximo passivo) e o mais seguro (mínimo passivo) em tempo constante $\mathcal{O}(1)$, atualizando passivos em $\mathcal{O}(\log N)$. Com isso, são disparadas defesas automáticas que estabilizam a operação.

---

## 🏗️ A Estrutura: Min-Max Heap Indexada

Uma **Min-Max Heap** é uma árvore binária completa que intercala níveis de mínimo e máximo:
- **Níveis Pares (0, 2, ...):** Níveis de **MÍNIMO**. O elemento raiz (índice 0) é garantidamente a chave de menor valor na estrutura.
- **Níveis Ímpares (1, 3, ...):** Níveis de **MÁXIMO**. Os filhos da raiz (índices 1 e 2) contêm o maior elemento da estrutura.

### Mapeamento Direto por Índice (`pos_map`)
Diferente de heaps convencionais onde a busca por um elemento arbitrário é $\mathcal{O}(N)$, a **Min-Max Heap Indexada** mantém uma tabela de ponteiros diretos (`pos_map[milhar] = indice_no_heap`). Isso permite:
1. Encontrar a posição de qualquer um dos 10.000 milhares em $\mathcal{O}(1)$;
2. Atualizar o passivo acumulado e restabelecer a propriedade do heap via *sift-up* ou *sift-down* em $\mathcal{O}(\log N)$.

### ⏱️ Complexidade Assintótica

| Operação | Vetor Linear Tradicional | Min-Max Heap Indexada | Impacto no Sistema |
| :--- | :---: | :---: | :--- |
| **Consultar Maior Risco (`peek_max`)** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Inspeção instantânea de teto |
| **Consultar Menor Risco (`peek_min`)** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Seleção imediata para balanceamento |
| **Consultar Milhar Específico** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Verificação de bilhete individual |
| **Atualizar Aposta / Passivo** | $\mathcal{O}(1)$ | $\mathcal{O}(\log N)$ | Manutenção da ordem em tempo real |
| **Identificar Ambos os Extremos** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Cálculo dinâmico de spreads |

---

## 🛡️ As 4 Estratégias de Defesa Ativa

Com a leitura em $\mathcal{O}(1)$ dos extremos de passivo, o sistema implementa 4 defesas em tempo real durante a submissão de cada aposta:

1. **Repasse de Risco (*Descarrego / Hedging*):**
   - Ao atingir um primeiro patamar de risco (`teto_descarrego`), a banca retém apenas a parcela segura e repassa o excedente a bancas parceiras, garantindo que o passivo retido não exceda o teto.
2. **Travamento (*Hard Cap / Circuit Breaker*):**
   - Se o passivo potencial ultrapassar o limite crítico de segurança (`teto_hard_cap`), a aposta é terminantemente bloqueada para impedir exposição descontrolada.
3. **Surpresinhas Inteligentes (Rebalanceamento Ativo):**
   - Quando o apostador opta pela modalidade "Surpresinha", o sistema direciona o palpite diretamente para a raiz da heap (`peek_min()`, $\mathcal{O}(1)$). Isso injeta volume nos números com menor passivo, equilibrando a carteira.
4. **Cotas Dinâmicas (*Dynamic Odds*):**
   - Avalia a razão entre o passivo atual e a amplitude $[mínimo, máximo]$. Números superaquecidos sofrem redução de cotação (ex: 3.200x), desestimulando a aposta, enquanto números frios recebem bônus (ex: 4.300x), atraindo liquidez.

---

## 📊 Resultados e Benchmarks

Os testes foram executados via script de simulação e benchmark integrado (`main.py`):

### 1. Desempenho Computacional (Streaming de 100.000 Apostas)
Simulação de alta frequência com 1.000 consultas aos extremos da banca:

* **Varredura Linear Tradicional $\mathcal{O}(N)$:** ~`524.43 ms`
* **Min-Max Heap Indexada $\mathcal{O}(1)$:** ~`262.48 ms`
* 🚀 **Ganho de Velocidade (*Speedup*):** **~2.00x mais rápido**

### 2. Simulação Monte Carlo (Solvência e Balanço Financeiro)
Execução de **1.000 dias operacionais** com **20.000 apostas/dia** e caixa inicial de **R$ 100.000,00**, com 30% do fluxo concentrado em números populares:

| Indicador | Modelo Tradicional (Reativo) | Modelo Min-Max Heap (Mitigado) |
| :--- | :---: | :---: |
| **Taxa de Falência (Quebra)** | **2.00%** (20 quebras em 1000 dias) | **0.00%** (0 quebras em 1000 dias) |
| **Pior Resultado Histórico** | **-R$ 29.879.822,00** (Ruína total) | **+R$ 105.184,24** (Lucro garantido) |
| **Saldo Mediano Final** | R$ 396.080,50 | R$ 158.456,46 |
| **Média de Intervenções/Dia** | 0 intervenções | ~6.689 descarregos / ~5.645 travamentos |

> **Conclusão:** O modelo tradicional aufere lucros nominais maiores em dias favoráveis, porém é matematicamente insustentável a longo prazo devido ao risco de cauda (*tail risk*). O modelo com Min-Max Heap abdica de margens excessivas via descarrego para manter a solvência garantida (0% de quebra).

---

## 📁 Estrutura do Projeto

```text
.
├── main.py             # Ponto de entrada: executa o benchmark e o Monte Carlo
├── src/
│   ├── __init__.py     # Pacote Python
│   ├── heap.py         # Implementação da IndexedMinMaxHeap e lógica de sifts
│   ├── modelos.py      # Classes BancaTradicional e BancaMitigadaMinMax
│   └── simulador.py    # Geração de fluxo sintético, benchmark e simulação Monte Carlo
├── .gitignore          # Arquivos e diretórios ignorados pelo Git
└── README.md           # Documentação completa do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior (sem dependências externas necessárias, utiliza apenas a biblioteca padrão `random`, `statistics`, `time`, `math`).

### Execução

Basta clonar o repositório e executar o script principal:

```bash
# Executar os experimentos
python3 main.py
```

---

## 👨‍💻 Autor

- **Gabriel França** ([@gb-franca](https://github.com/gb-franca))
- Curso de Tecnologia da Informação / Engenharia de Software - UFRN
- Disciplina: Estruturas de Dados Básicas II (EDB2)
