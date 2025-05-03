# Bin Packing com e sem Incerteza – Otimização sob Condições de Incertezas

Este repositório contém a implementação de dois modelos de otimização para resolver o problema de **bin packing** (empacotamento de itens), desenvolvido como parte das atividades da disciplina **Otimização sob Condições de Incertezas** do CEFET-MG.

## 🎯 Objetivo do Problema

O problema de *bin packing* consiste em alocar um conjunto de itens com pesos específicos em um número mínimo de "bins" (recipientes), respeitando a capacidade máxima de cada bin. Trata-se de um problema clássico de otimização combinatória com aplicações em logística, corte de materiais e computação em nuvem.

Neste trabalho, abordamos dois cenários distintos:

1. **Cenário Nominal:** pesos conhecidos e fixos.
2. **Cenário Robusto:** pesos sujeitos a incerteza, modelados por conjuntos poliedrais.

---

## 📁 Estrutura dos Códigos

### 1. `binpacking_nominal.py` — Modelo Nominal

Resolve o problema tradicional de bin packing com pesos fixos.

* **Ferramenta de modelagem:** `docplex.mp` (API Python do CPLEX)
* **Variáveis:**

  * `x_ij`: binária, indica se o item *i* está no bin *j*
  * `y_j`: binária, indica se o bin *j* é utilizado
* **Função objetivo:** minimizar o número de bins utilizados
* **Restrições:**

  * Cada item deve ser alocado a exatamente um bin
  * A soma dos pesos dos itens em cada bin deve ser menor ou igual à capacidade `C`

### 2. `binpacking_poliedrais.py` — Modelo Robusto com Incertezas Poliedrais

Estende o modelo anterior com proteção contra incertezas nos pesos dos itens, aplicando a abordagem de **programação robusta poliedral** inspirada em Bertsimas e Sim.

* **Novas variáveis:**

  * `rho_ij`, `z_j`: variáveis contínuas para representar os desvios dos pesos esperados
* **Parâmetros adicionais:**

  * `w_d`: desvios máximos dos pesos
  * `gamma_j`: grau de conservadorismo (quantos desvios simultâneos considerar por bin)
* **Restrições adicionais:**

  * Ajustam a capacidade dos bins para resistir ao pior caso de combinação de desvios
* **Objetivo:** continua sendo minimizar o número de bins

---

## ⚙️ Ferramenta de Otimização

* **Solver:** IBM CPLEX Optimizer
* **Interface utilizada:** `docplex.mp` (Modeling for Python)
* **Tipo de problema:** MILP (Mixed Integer Linear Programming)

---

## 📊 Resultados Obtidos

| Modelo                  | Bins Utilizados | Variáveis Totais                | Restrições Totais |
| ----------------------- | --------------- | ------------------------------- | ----------------- |
| **Nominal**             | 2               | 30                              | 10                |
| **Robusto (Poliedral)** | 5               | 60 (30 binárias + 30 contínuas) | 65                |

* O **modelo nominal** encontrou uma solução ótima utilizando apenas **2 bins**, já que considera apenas os pesos médios dos itens.
* O **modelo robusto** precisou de **5 bins** para acomodar os mesmos itens, pois adiciona salvaguardas contra desvios possíveis nos pesos — exigindo mais espaço total para garantir viabilidade sob incertezas.
* As variáveis `rho_ij` mostram o quanto cada item pode "inflar" seu peso, e `z_j` controla o impacto acumulado.

---

## 🧠 Conclusões

* A modelagem robusta é essencial quando há incerteza nos parâmetros do problema, especialmente em aplicações sensíveis como logística, onde subestimar pesos pode inviabilizar a operação.
* O custo da robustez é visível: **mais bins são utilizados** para garantir viabilidade em todos os cenários esperados.
* A abordagem poliedral permite ajustar o nível de proteção via o parâmetro `gamma`, oferecendo um bom compromisso entre conservadorismo e custo.

---

## 📚 Referências

* Bertsimas, D., & Sim, M. (2004). *The Price of Robustness*. Operations Research.
* Mingozzi, A., et al. (1999). *An exact algorithm for the two-dimensional finite bin packing problem*.
* IBM ILOG CPLEX Documentation: [https://www.ibm.com/docs/en/icos](https://www.ibm.com/docs/en/icos)