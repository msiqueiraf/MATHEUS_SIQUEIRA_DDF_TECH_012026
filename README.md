# Case Técnico Dadosfera - Analista de Dados

**Candidato:** Matheus Siqueira
**Data:** Janeiro/2026
**Repositório:** MATHEUS_SIQUEIRA_DDF_TECH_012026

---

## 📋 Item 0: Agilidade e Planejamento

Utilizei uma abordagem Ágil (Kanban) para organizar as entregas deste case, focando primeiro na infraestrutura de dados e posteriormente na camada de inteligência e visualização.

### 📅 Kanban Board do Projeto

#### 📝 Backlog (A Fazer)
- [ ] **Item 8:** Configurar Pipeline de Transformação (ETL) na Dadosfera
- [ ] **Item 9:** Desenvolver Data App em Streamlit
- [ ] **Item 10:** Gravação do Vídeo de Apresentação

#### 🚧 Doing (Em Andamento)
- [x] **Item 7:** Construção do Dashboard Analítico (Power BI)

#### ✅ Done (Concluído)
- [x] **Item 0:** Planejamento e Definição de Arquitetura
- [x] **Item 1:** Seleção do Dataset (Brazilian E-Commerce Olist)
- [x] **Item 2:** Ingestão de Dados na Plataforma Dadosfera
- [x] **Item 3:** Catalogação e Dicionário de Dados
- [x] **Item 4:** Validação de Qualidade de Dados (Great Expectations)
- [x] **Item 5:** Enriquecimento com IA (Feature Engineering / NLP)
- [x] **Item 6:** Modelagem Dimensional (Star Schema)

---

## 💾 Item 1: Sobre a Base de Dados

Para simular um cenário real de **E-commerce Brasileiro** com alta complexidade e volume (>100k registros), selecionei o **Brazilian E-Commerce Public Dataset by Olist**.

* **Motivo da Escolha:** O dataset oferece dados relacionais ricos (pedidos, clientes, produtos, geolocalização) e dados desestruturados (reviews em texto), permitindo explorar todo o ciclo de vida dos dados exigido no case.
* **Volume:** A tabela principal `order_items` possui mais de 112.000 registros.

---

## 🔌 Item 2 & 3: Integração e Exploração (Dadosfera)

Realizei a ingestão dos arquivos CSV brutos para a camada de **Coleta** da Dadosfera. Os dados foram catalogados com descrições funcionais para facilitar o self-service analytics por usuários de negócio.

**Evidência da Carga e Catalogação na Plataforma:**
![Print da Dadosfera - Ingestão](assets/item23_coleta_dadosfera.png)

---

## 🕵️ Item 4: Data Quality

Utilizei a biblioteca **Great Expectations** (versão Python) para implementar testes automatizados de qualidade de dados, gerando um relatório técnico de auditoria antes do consumo dos dados.

**Regras de Auditoria:**
1.  **Consistência de Domínio:** `expect_column_values_to_be_between(1, 5)` na coluna `review_score` para garantir que as notas sigam a regra de negócio.
2.  **Integridade Referencial:** `expect_column_values_to_not_be_null` na coluna `review_id` para assegurar unicidade e rastreabilidade.

**Evidência do Relatório de Qualidade:**
![Relatório de Data Quality](assets/item4_data_quality.png)

---

## 🤖 Item 5: Enriquecimento de Dados com IA (NLP)

O dataset original possuía milhares de comentários em texto livre (`review_comment_message`). Dados desestruturados são difíceis de analisar quantitativamente em Dashboards.

**Solução Aplicada:**
Desenvolvi um pipeline de **Feature Engineering** utilizando **Processamento de Linguagem Natural (NLP)** para transformar texto em dados estruturados.

* **Entrada (Input):** Texto bruto do cliente.
* **Processamento:** Algoritmo de classificação de sentimento (Polaridade e Regras de Negócio).
* **Saída (Output):** Nova dimensão `Sentimento` (Positivo 🟢 / Neutro 🟡 / Negativo 🔴).
* **Volume Processado:** Amostra estatística de 1.000 registros auditados.

**Evidência do Pipeline de NLP:**
![Output do Script de IA](assets/item5_nlp.png)

---

## 📐 Item 6: Modelagem de Dados

Desenvolvi uma modelagem **Star Schema (Fato/Dimensão)** no Power BI para garantir alta performance nas consultas e facilidade de uso para o usuário final. Adotei a nomenclatura padrão de Data Warehousing (`d` para dimensões, `f` para fatos).

* **Tabela Fato:** `fOrderItems` (Métricas: Vendas, Frete, Quantidade).
* **Dimensões:** `dCustomers`, `dProducts`, `dOrders`, `dReviews`.
* **Cardinalidade:** Relacionamentos `1 para *` (One-to-Many) fluindo das dimensões para a fato.

**Diagrama de Entidade-Relacionamento (DER):**
![Modelagem Star Schema](assets/item6_modelagem.png)

---

## 📊 Item 7 & Bônus 3: Análise de Dados (Power BI)

Optei por utilizar o **Power BI** (ferramenta externa) para entregar uma análise visual avançada e interativa, conforme sugerido no **Bônus 3** do case.

**Link para o Arquivo:** [Dashboard Power BI (.pbix)](./dashboard_analise_olist.pbix)

**Visualizações Desenvolvidas:**
1.  **KPIs Executivos:** Receita Total, Ticket Médio e Volumetria.
2.  **Análise Geoespacial:** Mapa de calor de vendas por Estado (Bônus 2).
3.  **Série Temporal:** Evolução de vendas por mês/ano.
4.  **Análise de Qualidade:** Distribuição das notas de satisfação (Enriquecida com os dados de Reviews).

**Preview do Dashboard:**
![Dashboard Final Power BI](assets/item7_dashboard.png)

---

## ⏭️ Próximos Passos (Roadmap)
- Finalização do Data App em Streamlit.
- Gravação do vídeo explicativo (Item 10).
