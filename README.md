# Case Técnico Dadosfera - Analista de Dados

**Candidato:** Matheus Siqueira  
**Data:** Janeiro/2026  
**Repositório:** MATHEUS_SIQUEIRA_DDF_TECH_012026  

---

## 📋 Item 0: Agilidade e Planejamento

Utilizei uma abordagem Ágil (Kanban) para organizar as entregas deste case, priorizando a infraestrutura de dados (Bronze/Silver) antes da camada de inteligência e visualização (Gold).

### 📅 Status do Projeto

#### ✅ Done (Concluído)
- [x] **Item 0:** Planejamento e Arquitetura
- [x] **Item 1:** Seleção do Dataset (Brazilian E-Commerce Olist)
- [x] **Item 2:** Ingestão de Dados na Plataforma Dadosfera
- [x] **Item 3:** Catalogação e Dicionário de Dados
- [x] **Item 4:** Validação de Qualidade de Dados (Great Expectations)
- [x] **Item 5:** Enriquecimento com IA (Feature Engineering / NLP)
- [x] **Item 6:** Modelagem Dimensional (Star Schema)
- [x] **Item 7:** Dashboard Analítico (Power BI)
- [x] **Item 8:** Orquestração de Pipelines (ETL)
- [x] **Item 9:** Data App Interativo (Streamlit)

#### 📹 To Do (A Fazer)
- [ ] **Item 10:** Gravação do Vídeo de Apresentação (Storytelling)

---

## 💾 Item 1: Sobre a Base de Dados

Para simular um cenário real de **E-commerce Brasileiro** com alta complexidade e volume (>100k registros), selecionei o **Brazilian E-Commerce Public Dataset by Olist**.

* **Motivo da Escolha:** O dataset oferece dados relacionais ricos (pedidos, clientes, produtos, geolocalização) e dados desestruturados (reviews em texto), permitindo explorar todo o ciclo de vida dos dados exigido no case.
* **Volume:** A tabela principal `order_items` possui mais de 112.000 registros, atendendo ao requisito mínimo do case.

---

## 🔌 Item 2 & 3: Integração e Exploração (Dadosfera)

Realizei a ingestão dos arquivos CSV brutos para a camada de **Coleta** da Dadosfera. Os dados foram catalogados com descrições funcionais e técnicas para facilitar o self-service analytics por usuários de negócio.

> 📘 **Documentação Técnica:** Para detalhes aprofundados sobre a linhagem, tipagem e regras de negócio aplicadas em cada tabela (Silver/Gold), consulte o **[Dicionário de Dados Técnico](./DATA_DICTIONARY.md)**.

**Evidência da Carga e Catalogação na Plataforma:**
![Print da Dadosfera - Ingestão](assets/item23_coleta_dadosfera.png)

---

## 🕵️ Item 4: Data Quality (Observabilidade)

Implementei um pipeline de auditoria automatizada fundamentado em **Data Contracts** e observabilidade de dados. Utilizei uma lógica de validação inspirada no framework *Great Expectations* para garantir que apenas dados íntegros e confiáveis avancem para a camada de modelagem. Todo o motor de auditoria e monitoramento está centralizado no arquivo **`data_quality.py`** na raiz do repositório.

**Regras de Auditoria Aplicadas:**
* **Consistência de Domínio:** Validação estatística rigorosa para garantir que a coluna `review_score` esteja dentro do intervalo esperado de **1 a 5**.
* **Integridade Referencial:** Check de completude na **Chave Primária** `review_id` (Zero Nulls), assegurando a unicidade e rastreabilidade total dos registros.
* **Health Check & Monitoring:** Geração automática de métricas descritivas (Mínimo, Máximo e Média) para monitoramento de saúde da base e detecção precoce de anomalias.

**Evidência do Relatório de Qualidade:**
![Relatório de Data Quality](assets/item4_data_quality.png)

---

## 🤖 Item 5: Enriquecimento com IA (Advanced NLP no Power Query)

Para processar o volume de textos desestruturados (`review_comment_message`), desenvolvi um motor de **NLP** robusto utilizando a biblioteca **spaCy** (modelo `pt_core_news_sm`).

**Diferencial Técnico: Motor de Inferência Híbrida**
Implementei uma **Calibração de Ground Truth**, onde o algoritmo correlaciona a semântica extraída via IA com a nota real deixada pelo cliente, calibrando a polaridade final para refletir a experiência real do usuário.

**Integração e Portabilidade:**
A lógica está encapsulada no script **`power_query_nlp.py`**. O código foi portado para o ambiente do **Power Query (Python Step)**, permitindo o enriquecimento dinâmico do modelo de dados diretamente no Power BI a cada refresh.

* **Otimização Upstream:** Implementei uma filtragem prévia no Power Query para enviar ao script Python apenas as colunas estritamente necessárias (`id`, `score`, `text`), reduzindo o tempo de processamento e serialização de dados.
* **Métricas de Saída:** Geração das colunas `Polaridade_IA` (-1.0 a +1.0) e `Sentimento_IA` (Positivo 🟢 / Neutro 🟡 / Negativo 🔴).

**Evidência da Integração no Power BI:**
![Script Python no Power Query](assets/powerquery_python_integration.png)

**Evidência do Pipeline de NLP:**
![Output do Script de IA](assets/item5_nlp.png)

---

## 📐 Item 6: Modelagem de Dados

Desenvolvi uma modelagem **Star Schema (Fato/Dimensão)** no Power BI para garantir alta performance nas consultas DAX e facilidade de uso para o usuário final.

### 🏗️ Engenharia de Dados e Performance (Silver Layer)
Apliquei conceitos avançados de engenharia na etapa de transformação (Power Query) para garantir escalabilidade e governança:

1.  **Governança (Naming Conventions):** Adotei estritamente o padrão **`snake_case`** (ex: `product_category_name` em vez de `Nome da Categoria`) e removi acentos/caracteres especiais.
    * *Motivo:* Garantir interoperabilidade imediata caso o modelo seja migrado para Data Lakes (Parquet/Delta) ou Bancos SQL, onde espaços e acentos costumam quebrar pipelines.
2.  **Vertical Partitioning (Performance):** Realizei a remoção agressiva de colunas de alta cardinalidade não utilizadas (ex: `customer_zip_code`, `product_description`) antes da carga.
    * *Impacto:* Redução drástica do consumo de memória do motor VertiPaq e aceleração do refresh.
3.  **Type Safety:** Garantia de tipagem forte, especialmente para dados monetários (`type number` para preservar centavos) e tratamento de locale (`en-US`) nos outputs do Python.

### Estrutura do Modelo
* **Tabela Fato (`fOrderItems`):** Contém os dados transacionais (granularidade por item vendido).
    * *Métricas:* Valor de Venda, Valor de Frete, Quantidade.
* **Dimensões (`d...`):** Tabelas auxiliares que fornecem contexto descritivo.
    * `dProducts` (Categorias higienizadas e padronizadas).
    * `dOrders` (Status e datas do ciclo de vida do pedido).
    * `dCustomers` (Localização geográfica por Estado/Cidade).
    * `dReviews` (Comentários e notas de satisfação enriquecidas via IA).

**Diagrama de Entidade-Relacionamento (DER):**
![Modelagem Star Schema](assets/item6_modelagem.png)

---

## 📊 Item 7 & Bônus 3: Análise de Dados (Power BI & SQL)

Para cumprir o requisito de análise exploratória e validação de categorias, utilizei o **SQL Lab** da Dadosfera (Engine Snowflake) antes de partir para a visualização no Power BI.

### 🔍 Validação Exploratória (SQL)
**Objetivo:** Validar a distribuição de produtos por categoria diretamente na fonte (Silver Layer), assegurando a integridade dos dados antes da modelagem.

**Evidência da Execução (Query + Resultado):**
![Resultado SQL](assets/item7_sql_query.png)

### 🚀 Dashboard Executivo (Power BI)
Para superar as expectativas de uma análise padrão, desenvolvi um **Dashboard Executivo de Alta Performance** no Power BI. O foco foi unir Engenharia de Dados robusta com uma experiência de usuário (UX) moderna e acionável.

**Link para o Arquivo:** [Dashboard Power BI (.pbix)](./dashboard_analise_olist.pbix)

#### Destaques de Engenharia e Performance
* **Otimização da Dimensão Tempo (`dTime`):** Implementei uma tabela dimensão otimizada com granularidade de **minutos** (1.440 linhas) em vez de segundos (86.400 linhas). Isso reduz a cardinalidade e melhora a performance do motor VertiPaq, mantendo a precisão necessária para análises de pico de horário (ex: "Horário de Almoço").
* **Controle de Filtragem (DAX Avançado):** Evitei relacionamentos bidirecionais físicos (que impactam performance). Utilizei a função **`CROSSFILTER`** via DAX para propagar filtros complexos (ex: *Categoria do Produto* impactando *SLA do Pedido*) apenas no momento do cálculo.

#### UX/UI Avançado (HTML & CSS Dinâmico)
Em vez dos cartões nativos limitados, desenvolvi um **Header Dinâmico via HTML/SVG** injetado via DAX.
* **Visual:** Estilo *Glassmorphism* (Efeito de vidro) com sombras e bordas arredondadas via CSS.
* **KPIs da Tríade de Vendas:** Faturamento (com formatação automática de "Bi/Mi"), Volume de Pedidos e Ticket Médio.
* **Indicadores de Contexto:** Ícones SVG que mudam de cor e forma automaticamente baseados nos dados (ex: o ícone de Sentimento vira um "Joinha para baixo" vermelho se a aprovação cair, alertando o gestor visualmente).

#### Inteligência Artificial Acionável
Integrei os outputs do modelo de NLP diretamente na camada visual:
* **Monitor de Sentimento:** Um KPI exclusivo que traduz a "Polaridade Matemática" (-1 a 1) para linguagem de negócio ("Positivo", "Atenção", "Negativo"), permitindo que diretores identifiquem crises de reputação em tempo real.

**Preview do Dashboard:**
![Dashboard Final Power BI](assets/item7_dashboard.png)

---

## 🌊 Item 8: Pipeline de Dados (Orquestração)

Para garantir a atualização contínua e a governança dos dados, desenhei um pipeline de ingestão na Dadosfera que automatiza a coleta dos arquivos brutos (Raw Data).

**Fluxo Desenhado:**
1. **Coleta:** Leitura incremental de arquivos CSV em Bucket S3.
2. **Ingestão:** Carga para a Landing Zone da Dadosfera.
3. **Catalogação:** Registro automático de metadados técnicos.
4. **Agendamento:** Execução diária automatizada.

**Evidência do Pipeline Catalogado:**
![Pipeline Dadosfera](assets/item8_pipeline.png)

---

## 📱 Item 9: Data App (Streamlit)

Desenvolvi uma aplicação interativa utilizando o framework **Streamlit** (Python) para democratizar o acesso aos dados de satisfação. O app permite que gestores filtrem reviews por região e acompanhem KPIs em tempo real.

**Funcionalidades:**
* Filtros Dinâmicos de Região.
* Formatação monetária padrão BRL (R$).
* Comparativo de Metas (vs Mês Anterior).
* Visualização Dark Mode para alto contraste.

**Preview do App:**
![Data App Streamlit](assets/item9_data_app.png)

### 🛠️ Como Executar este Data App
O desenvolvimento foi realizado utilizando o **Google Colab**. Para reproduzir localmente:

1. **Pré-requisitos:** Python 3.9+, Streamlit, Pandas e Plotly.
2. **Instalação:** `pip install streamlit pandas plotly`.
3. **Execução:** Navegue até a pasta do projeto e execute no terminal: `streamlit run app.py`.
4. **Acesso Remoto (Cloud):** Utilizado túnel via **Ngrok** para deploy simulado durante o desenvolvimento.

---

## ⏭️ Próximos Passos (Roadmap)
- Gravação do vídeo de apresentação executiva (Item 10).
- Implementação de alertas automáticos via Slack/Teams baseados na queda do NPS.
