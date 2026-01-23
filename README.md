# 🚀 Case Técnico Dadosfera - Analista de Dados

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
- [x] **Item 5:** Enriquecimento com IA (Análise de Sentimento)
- [x] **Item 6:** Modelagem Dimensional (Star Schema)

---

## 💾 Item 1: Sobre a Base de Dados

Para simular um cenário real de **E-commerce Brasileiro** com alta complexidade e volume (>100k registros), selecionei o **Brazilian E-Commerce Public Dataset by Olist**.

* **Motivo da Escolha:** O dataset oferece dados relacionais ricos (pedidos, clientes, produtos, geolocalização) e dados desestruturados (reviews em texto), permitindo explorar todo o ciclo de vida dos dados exigido no case.
* **Volume:** A tabela principal `order_items` possui mais de 112.000 registros.

---

## 🔌 Item 2 & 3: Integração e Exploração (Dadosfera)

Realizei a ingestão dos arquivos CSV brutos para a camada de **Coleta** da Dadosfera. Os dados foram catalogados com descrições funcionais para facilitar o self-service analytics.

**Evidência da Carga e Catalogação na Plataforma:**
*(Insira aqui o print da tela "Coletar" com os arquivos listados)*
![Print da Dadosfera - Ingestão](nome_do_seu_print_dadosfera.png)

---

## 🕵️ Item 4: Data Quality

Utilizei **Python** para rodar um script de validação de dados, simulando as regras da biblioteca `great_expectations`.

**Regras Validadas:**
1.  **Consistência de Notas:** Garantir que `review_score` esteja sempre entre 1 e 5.
2.  **Integridade de Chaves:** Garantir que não existam `review_id` nulos.

**Evidência do Relatório de Qualidade:**
*(Insira aqui o print do Colab com os "Checks" verdes)*
![Relatório de Data Quality](nome_do_seu_print_quality.png)

---

## 🤖 Item 5: GenAI e Enriquecimento (NLP)

Para transformar dados desestruturados (texto livre dos reviews) em dados estruturados (Features), desenvolvi um pipeline de **Processamento de Linguagem Natural (NLP)**.

* **Input:** Texto do comentário (`review_comment_message`).
* **Processamento:** Análise de sentimento e correlação com a nota.
* **Output:** Nova feature `Sentimento` (Positivo, Negativo, Neutro) e Log de Contexto.

**Evidência do Processamento com IA:**
*(Insira aqui o print do Colab mostrando a classificação dos 10 reviews)*
![Output do Script de IA](nome_do_seu_print_ia.png)

---

## 📐 Item 6: Modelagem de Dados

Desenvolvi uma modelagem **Star Schema (Fato/Dimensão)** para otimizar a performance analítica no Power BI.

* **Tabela Fato:** `f_order_items` (Transações, Valores, Frete).
* **Dimensões:** `d_products`, `d_customers`, `d_orders`, `d_reviews`.
* **Relacionamento:** Esquema `1 para *` (One-to-Many) fluindo das dimensões para a fato.

**Diagrama de Entidade-Relacionamento (DER):**
*(Insira aqui o print do diagrama do Power BI que arrumamos)*
![Modelagem Star Schema](nome_do_seu_print_modelagem.png)

---

## 📊 Item 7 & Bônus 3: Análise de Dados (Power BI)

Optei por utilizar o **Power BI** (ferramenta externa) para entregar uma análise visual avançada e interativa, conforme sugerido no **Bônus 3**.

**Link para o Arquivo:** [Dashboard Power BI (.pbix)](./nome_do_arquivo.pbix)

**Visualizações Desenvolvidas:**
1.  **KPIs Executivos:** Receita Total, Ticket Médio e Volumetria.
2.  **Análise Geoespacial:** Mapa de calor de vendas por Estado (Bônus 2).
3.  **Série Temporal:** Evolução de vendas por mês/ano.
4.  **Análise de Qualidade:** Distribuição das notas de satisfação dos clientes.

**Preview do Dashboard:**
*(Insira aqui o print final do Dashboard que vamos tirar agora)*
![Dashboard Final Power BI](nome_do_seu_print_dashboard.png)

---

## ⏭️ Próximos Passos (Roadmap)
- Finalização do Data App em Streamlit.
- Gravação do vídeo explicativo (Item 10).
