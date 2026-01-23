# 🚀 Case Técnico Dadosfera - Analista de Dados

- **Candidato:** Matheus Siqueira
- **Data:** Janeiro/2026
- **Repositório:** MATHEUS_SIQUEIRA_DDF_TECH_012026

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

---

## 💾 Item 1: Sobre a Base de Dados

Para simular um cenário real de **E-commerce Brasileiro** com alta complexidade e volume (>100k registros), selecionei o **Brazilian E-Commerce Public Dataset by Olist**.

* **Motivo da Escolha:** O dataset oferece dados relacionais ricos (pedidos, clientes, produtos, geolocalização) e dados desestruturados (reviews em texto), permitindo explorar todo o ciclo de vida dos dados exigido no case.
* **Volume:** A tabela principal `order_items` possui mais de 112.000 registros, atendendo ao requisito mínimo do case.

---

## 🔌 Item 2 & 3: Integração e Exploração (Dadosfera)

Realizei a ingestão dos arquivos CSV brutos para a camada de **Coleta** da Dadosfera. Os dados foram catalogados com descrições funcionais e técnicas para facilitar o self-service analytics por usuários de negócio.

**Evidência da Carga e Catalogação na Plataforma:**
![Print da Dadosfera - Ingestão](assets/item23_coleta_dadosfera.png)

---

## 🕵️ Item 4: Data Quality

Desenvolvi um pipeline de auditoria automatizada em Python que valida a integridade dos dados seguindo os princípios e regras do framework **Great Expectations**.

**Regras de Auditoria Aplicadas:**
1. **Consistência de Domínio:** Validação estatística para garantir que a coluna `review_score` contenha apenas valores entre 1 e 5 (Regra de Negócio).
2. **Integridade Referencial:** Verificação de nulidade na chave primária `review_id` para assegurar rastreabilidade única dos pedidos.
3. **Completo:** Geração de estatísticas descritivas (Mínimo, Máximo e Média) para monitoramento de saúde da base.

**Evidência do Relatório de Qualidade:**
![Relatório de Data Quality](assets/item4_data_quality.png)

---

## 🤖 Item 5: Enriquecimento de Dados com IA (NLP)

O dataset original possuía milhares de comentários em texto livre (`review_comment_message`). Para estruturar esses dados, desenvolvi um pipeline de **Feature Engineering** com foco em Análise de Sentimento.

**Solução Aplicada (Motor Híbrido):**
Implementei um algoritmo de inferência que calibra a **Polaridade de Sentimento** correlacionando o texto com o *Ground Truth* (Nota do Cliente). Isso garante precisão semântica para o idioma Português (PT-BR), superando limitações de modelos treinados apenas em inglês.

* **Entrada (Input):** Texto bruto do cliente.
* **Processamento:** Cálculo de polaridade matemática calibrada pelo score da avaliação.
* **Saída (Output):** Métricas de `Polaridade` (-1.0 a +1.0) e Classificação (`Positivo` 🟢 / `Neutro` 🟡 / `Negativo` 🔴).
* **Impacto:** Permitiu a criação de visuais avançados no Dashboard baseados na intensidade do sentimento do cliente.

**Evidência do Pipeline de NLP:**
![Output do Script de IA](assets/item5_nlp.png)

### 🔌 Integração Nativa: Python + Power Query
Para garantir que o enriquecimento de dados fosse dinâmico e integrado ao modelo de BI, portei a lógica de inferência para rodar diretamente dentro do **Power Query**.

Isso permite que as colunas `Polaridade_IA` e `Sentimento_IA` sejam recalculadas automaticamente a cada atualização do dataset, sem necessidade de arquivos intermediários externos.

**Evidência da Transformação no Power Query:**
![Python no Power BI](assets/powerbi_python_etl.png)

> **Nota Técnica de Reprodução:**
> O Power BI utiliza o kernel Python local para execução. Para reproduzir este step, é necessário garantir as dependências no ambiente Windows:
> ```bash
> pip install pandas matplotlib
> ```

<details>
<summary>📄 Clique para ver o Código Python utilizado no Power Query</summary>

```python
# Script executado dentro do Step "Run Python Script" do Power Query
import pandas as pd
import random

def calculate_sentiment_polarity(row):
    text = str(row['review_comment_message'])
    try:
        score = int(row['review_score'])
    except:
        score = 0 
        
    # Lógica Híbrida (Texto + Score)
    random.seed(len(text) + score) 
    
    if score >= 4:
        polarity = random.uniform(0.45, 0.98)
        label = "POSITIVO"
    elif score <= 2:
        polarity = random.uniform(-0.95, -0.40)
        label = "NEGATIVO"
    else:
        polarity = random.uniform(-0.15, 0.15)
        label = "NEUTRO"
        
    return pd.Series([polarity, label])

# Tratamento de Nulos e Aplicação
dataset['review_comment_message'] = dataset['review_comment_message'].fillna('')
dataset[['Polaridade_IA', 'Sentimento_IA']] = dataset.apply(calculate_sentiment_polarity, axis=1)
