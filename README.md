# 📊 Planejamento do Projeto - Case Técnico Dadosfera

## 📅 Metodologia Ágil (Kanban)

### 📝 Backlog (A Fazer)
- [ ] **Item 8:** Configurar Pipeline de Transformação (ETL) na Dadosfera
- [ ] **Item 9:** Desenvolver Data App em Streamlit (Simulador de Custos)
- [ ] **Bônus:** Integração com Power BI para análise executiva

### 🚧 Doing (Em Andamento)
- [x] **Item 0:** Planejamento e Definição de Arquitetura (PMBOK)
- [x] **Item 1:** Seleção do Dataset (Brazilian E-Commerce Olist)
- [ ] **Item 2:** Ingestão de Dados na Plataforma Dadosfera (>100k registros)
- [ ] **Item 3:** Catalogação e Dicionário de Dados
- [ ] **Item 5:** Enriquecimento com IA (Análise de Sentimento dos Reviews)

### ✅ Done (Concluído)
- [x] Leitura e entendimento do Case Técnico

---

## ⚠️ Análise de Riscos e Recursos

| Risco | Impacto | Mitigação |
| :--- | :--- | :--- |
| **Inconsistência nos Dados** | Alto (Pode gerar análises erradas) | Utilizar biblioteca Great Expectations (Item 4) para validar tipos e nulos. |
| **Custo de Processamento (IA)** | Médio (Uso de APIs pagas) | Utilizar amostragem de dados para teste de conceito (PoC) antes do processamento total. |
| **Prazo de Entrega** | Alto | Priorizar o fluxo: Ingestão -> Visualização -> IA -> App. |

## 💰 Estimativa de Recursos
- **Humano:** 1 Analista de Dados Sênior (Full-stack).
- **Infraestrutura:** Ambiente SaaS Dadosfera (Armazenamento + Compute) + Google Colab (Python/AI).
- **Tempo:** Sprint de 5 dias úteis.
