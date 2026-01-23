import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="Data App Olist", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado para Tema Dark/Profissional
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    
    /* Estilização dos Cards de Métricas */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #41424C;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* Cor dos valores numéricos */
    div[data-testid="stMetricValue"] {
        color: #00D4FF !important;
    }
    
    /* Centralização de títulos */
    h1, h2, h3 {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNÇÕES AUXILIARES E CARGA DE DADOS
# ==============================================================================

def formatar_moeda(valor):
    """Formata valores float para o padrão monetário BRL (R$ 1.000,00)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data
def carregar_dados():
    """
    Gera dados simulados para o dashboard. 
    O decorator @st.cache_data garante performance e consistência.
    """
    np.random.seed(42)
    qtd_registros = 500
    
    regioes_possiveis = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']
    # Pesos ajustados para realismo (maior volume onde há mais população)
    notas_possiveis = [5, 5, 5, 4, 4, 3, 2, 1] 
    status_possiveis = ['No Prazo', 'No Prazo', 'No Prazo', 'Atrasado', 'Extraviado']

    data = {
        'Nota': np.random.choice(notas_possiveis, qtd_registros),
        'Status': np.random.choice(status_possiveis, qtd_registros),
        'Regiao': np.random.choice(regioes_possiveis, qtd_registros),
        'Valor_Venda': np.random.uniform(50, 500, qtd_registros)
    }
    
    return pd.DataFrame(data)

# ==============================================================================
# 3. INTERFACE PRINCIPAL
# ==============================================================================

def main():
    # Cabeçalho
    st.title("🚀 Painel de Inteligência - Olist E-commerce")
    st.markdown("### Monitoramento de Satisfação e Performance Logística")
    st.divider()

    # Carga de Dados
    df = carregar_dados()

    # --- SIDEBAR (FILTROS) ---
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
    st.sidebar.markdown("## 🔎 Filtros Globais")
    
    filtro_regiao = st.sidebar.multiselect(
        "Selecione a Região:",
        options=df['Regiao'].unique(),
        default=df['Regiao'].unique()
    )

    # Aplicação do Filtro
    df_filtrado = df[df['Regiao'].isin(filtro_regiao)]

    # Tratamento de erro para filtro vazio
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    # --- CÁLCULO DE KPIS ---
    total_vendas = df_filtrado['Valor_Venda'].sum()
    total_reviews = len(df_filtrado)
    
    # Cálculo de NPS Simplificado (Baseado em notas 4 e 5 como promotores)
    nps_score = int((len(df_filtrado[df_filtrado['Nota'] >= 4]) / total_reviews) * 100)
    prazo_medio = 4.2 # Constante simulada

    # --- EXIBIÇÃO DE METRICAS ---
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Receita Total", formatar_moeda(total_vendas), "vs. Mês Anterior")
    col2.metric("Total de Reviews", f"{total_reviews}", "+120 esta semana")
    col3.metric("NPS (Satisfação)", f"{nps_score}", "+2 pts vs Meta")
    col4.metric("Prazo Médio", f"{prazo_medio} Dias", "-0.8 dias (Melhoria)")

    st.markdown("---")

    # --- VISUALIZAÇÕES GRÁFICAS ---
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### ⭐ Distribuição de Notas")
        distribuicao = df_filtrado['Nota'].value_counts().sort_index()
        
        fig = px.bar(
            x=distribuicao.index, 
            y=distribuicao.values,
            labels={'x': 'Nota (1-5)', 'y': 'Qtd Reviews'},
            color_discrete_sequence=['#00D4FF'],
            template="plotly_dark"
        )
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 📦 Status dos Pedidos")
        fig2 = px.pie(
            df_filtrado, 
            names='Status', 
            hole=0.5, 
            color_discrete_sequence=['#00D4FF', '#FF4B4B', '#FFC300'],
            template="plotly_dark"
        )
        fig2.update_layout(margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.info("Desenvolvido por Matheus Siqueira | Case Técnico Dadosfera")

if __name__ == "__main__":
    main()
