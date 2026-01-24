# 📚 Dicionário de Dados (Camada Silver/Gold)

Este documento detalha a estrutura tabular do modelo analítico após os processos de Engenharia de Dados e Enriquecimento.

---

## 1. Fatos

### 📦 `fOrderItems`
Tabela transacional contendo a granularidade de itens por pedido. Filtros de alta cardinalidade foram removidos para otimização (Vertical Partitioning).

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `order_id` | `text` | Chave única do pedido. | FK para `dOrders`. |
| `product_id` | `text` | Chave do produto. | FK para `dProducts`. |
| `price` | `number` | Valor unitário do item. | Mantido `decimal` para precisão de centavos. |
| `freight_value` | `number` | Valor do frete rateado por item. | - |

---

## 2. Dimensões

### 🛒 `dProducts`
Cadastro de produtos com categorias higienizadas.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `product_category_name` | `text` | Categoria macro do item. | 1. `null` substituído por "Outros".<br>2. Remoção de `_`.<br>3. Formatação Title Case (ex: "Cama Mesa Banho"). |

### 🚚 `dOrders`
Ciclo de vida logístico do pedido.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `order_status` | `text` | Situação atual (delivered, canceled, etc). | - |
| `order_purchase_timestamp` | `datetime` | Data/Hora exata da compra. | Base para cálculo de SLA. |
| `order_delivered_customer_date` | `datetime` | Data real da entrega. | Usado para KPI de SLA (Entrega vs Estimativa). |
| `order_estimated_delivery_date` | `datetime` | Data prometida ao cliente. | Target do SLA. |

### 🗣️ `dReviews` (Enriquecida com IA)
Avaliações dos clientes processadas por motor de NLP.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `review_score` | `int` | Nota original (1-5). | Dado bruto. |
| `review_comment_message` | `text` | Comentário escrito. | - |
| `Polaridade_IA` | `decimal` | Score de sentimento (-1.0 a +1.0). | **Cálculo Híbrido:** (Semântica NLP * 0.7) + (Calibração Score * 0.3).<br>Processado via Python/spaCy. |
| `Sentimento_IA` | `text` | Classificação de Negócio. | `Positivo` (> 0.15), `Negativo` (< -0.15), `Neutro` (resto). |

### ⏰ `dTime` (Dimensão Otimizada)
Eixo temporal intradia para análise de picos de venda. Granularidade: Minuto.

| Coluna | Tipo | Descrição | Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `day_period` | `text` | Turno comercial da venda. | **Madrugada:** 00h-06h<br>**Manhã:** 06h-12h<br>**Almoço:** 12h-14h (Pico de Vendas)<br>**Tarde:** 14h-18h<br>**Noite:** 18h-24h |

---
