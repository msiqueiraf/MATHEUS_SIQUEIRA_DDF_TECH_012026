# 📚 Dicionário de Dados (Camada Silver/Gold)

Este documento detalha a estrutura tabular do modelo analítico, incluindo metadados de linhagem, granularidade e regras de transformação aplicadas no Pipeline de Engenharia.

---

## 1. Fatos

### 📦 `fOrderItems`
**Metadados Técnicos**
> * **Fonte Original:** `olist_order_items.csv`
> * **Granularidade:** Uma linha por **Item** dentro de um Pedido (ex: Se um pedido tem 3 itens, haverá 3 linhas).
> * **Tipo de Carga:** Incremental.
> * **Volume Aproximado:** ~112k linhas.

Tabela transacional central. Filtros de alta cardinalidade foram removidos para otimização (Vertical Partitioning).

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `order_id` | `text` | Chave única do pedido. | FK para `dOrders`. |
| `product_id` | `text` | Chave do produto. | FK para `dProducts`. |
| `price` | `number` | Valor unitário do item. | **Safe Type:** Conversão forçada com Locale `en-US` para garantir precisão decimal (evitar erro de vírgula/ponto em valores monetários). |
| `freight_value` | `number` | Valor do frete rateado por item. | **Safe Type:** Conversão forçada com Locale `en-US`. |

---

## 2. Dimensões

### 🛒 `dProducts`
**Metadados Técnicos**
> * **Fonte Original:** `olist_products.csv`
> * **Granularidade:** Uma linha por SKU (Produto Único).
> * **Tratamento:** Higienização de strings para padronização visual.

Cadastro de produtos com categorias higienizadas.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `product_id` | `text` | ID único do produto. | PK da tabela. |
| `product_category_name` | `text` | Categoria macro do item. | 1. `null` substituído por "Outros".<br>2. Remoção de `_`.<br>3. Formatação Title Case (ex: "Cama Mesa Banho"). |

### 🚚 `dOrders`
**Metadados Técnicos**
> * **Fonte Original:** `olist_orders.csv`
> * **Granularidade:** Uma linha por Pedido (Order Head).
> * **Uso Principal:** Cálculo de SLA Logístico e Faturamento Temporal.

Ciclo de vida logístico do pedido.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `order_id` | `text` | Chave única do pedido. | PK da tabela. |
| `order_status` | `text` | Situação atual (delivered, canceled, etc). | - |
| `order_purchase_timestamp` | `datetime` | Data/Hora exata da compra. | Base para cálculo de SLA e Chave para `dCalendar` / `dTime`. |
| `order_approved_at` | `datetime` | Data de aprovação do pagamento. | - |
| `order_delivered_carrier_date` | `datetime` | Data de postagem na transportadora. | - |
| `order_delivered_customer_date` | `datetime` | Data real da entrega. | Usado para KPI de SLA (Entrega vs Estimativa). |
| `order_estimated_delivery_date` | `datetime` | Data prometida ao cliente. | Target do SLA. |

### 🗣️ `dReviews` (Enriquecida com IA)
**Metadados Técnicos**
> * **Fonte Original:** `olist_order_reviews.csv`
> * **Motor de Enriquecimento:** Python (spaCy) rodando no Power Query.
> * **Granularidade:** Uma linha por Avaliação.

Avaliações dos clientes processadas por motor de NLP.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `review_id` | `text` | ID da avaliação. | PK da tabela. |
| `order_id` | `text` | ID do pedido avaliado. | FK para `dOrders`. |
| `review_score` | `int` | Nota original (1-5). | Dado bruto. |
| `review_comment_message` | `text` | Comentário escrito. | Filtrado na origem para remover nulos antes do NLP. |
| `Polaridade_IA` | `decimal` | Score de sentimento (-1.0 a +1.0). | **Cálculo Híbrido:** (Semântica NLP * 0.7) + (Calibração Score * 0.3).<br>Tipagem forçada para `en-US` (ponto decimal). |
| `Sentimento_IA` | `text` | Classificação de Negócio. | `Positivo` (> 0.15), `Negativo` (< -0.15), `Neutro` (resto). |

### 📍 `dCustomers` (Enriquecida - Geo)
**Metadados Técnicos**
> * **Fonte Original:** `olist_customers.csv`
> * **Fonte Auxiliar:** `olist_geolocation.csv` (Lookup Table).
> * **Privacidade (LGPD):** Dados anonimizados (apenas Região, sem Nome/CPF).
> * **Granularidade:** Uma linha por Cliente/Pedido.

Cadastro geográfico dos clientes enriquecido com Lat/Long exata.

| Coluna | Tipo | Descrição | Regra de Transformação |
| :--- | :--- | :--- | :--- |
| `customer_id` | `text` | ID do cliente vinculado ao pedido. | PK para ligação com `dOrders`. |
| `customer_unique_id` | `text` | ID único do cliente (CPF mascarado). | Usado para contagem distinta (Churn/Recorrência). |
| `customer_city` | `text` | Cidade de entrega. | Padronizada com `Text.Proper` (ex: "sao paulo" -> "Sao Paulo"). |
| `customer_state` | `text` | Sigla do Estado (UF). | - |
| `lat_media` | `decimal` | Latitude Média do CEP. | **Enriquecimento:** Merge com base de Geolocalização agrupada por CEP.<br>**Locale:** `en-US` para correção de ponto decimal. |
| `long_media` | `decimal` | Longitude Média do CEP. | **Enriquecimento:** Merge com base de Geolocalização. |

### ⏰ `dTime` (Dimensão Otimizada)
**Metadados Técnicos**
> * **Fonte Original:** Gerada via Script M (Calculada).
> * **Granularidade:** Minuto a Minuto (00:00 a 23:59).
> * **Performance:** Redução de cardinalidade (de Segundos para Minutos).

Eixo temporal intradia para análise de picos de venda.

| Coluna | Tipo | Descrição | Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `time` | `time` | Hora/Minuto (HH:MM:00). | Chave de ligação com `dOrders[order_purchase_time]`. |
| `day_period` | `text` | Turno comercial da venda. | **Madrugada:** 00h-06h<br>**Manhã:** 06h-12h<br>**Almoço:** 12h-14h (Pico de Vendas)<br>**Tarde:** 14h-18h<br>**Noite:** 18h-24h |
