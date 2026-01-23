"""
PIPELINE DE OBSERVABILIDADE E ENRIQUECIMENTO DE DADOS
Candidato: Matheus Siqueira
Projeto: Case Técnico Dadosfera - Brazilian E-Commerce (Olist)
"""

import pandas as pd
import sys
import os
import spacy

# ==============================================================================
# 1. SETUP E CARREGAMENTO DE MODELOS (IA/NLP)
# ==============================================================================
def load_nlp_model():
    """Garante o carregamento do modelo pt_core_news_sm do spaCy."""
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        print("ℹ️ Instalando modelo de linguagem pt_core_news_sm...")
        os.system("python -m spacy download pt_core_news_sm")
        return spacy.load("pt_core_news_sm")

nlp = load_nlp_model()

# ==============================================================================
# 2. MOTOR DE INFERÊNCIA HÍBRIDA (ITEM 5)
# ==============================================================================
def get_sentiment_engine(text, score):
    """
    Analisa o sentimento combinando semântica (NLP) com Ground Truth (Score).
    Retorna a polaridade normalizada e o rótulo alinhado para logs.
    """
    if pd.isna(text) or text.strip() == "":
        # Baseline matemático quando o comentário está ausente
        polarity = (score - 3) / 2
    else:
        # Processamento via spaCy (Tokenization e Lemmatization)
        doc = nlp(str(text).lower())
        pos_lemmas = ['bom', 'ótimo', 'excelente', 'rápido', 'recomendo', 'parabéns']
        neg_lemmas = ['ruim', 'péssimo', 'atraso', 'lento', 'horrível', 'quebrado']
        
        pos_count = sum(1 for t in doc if t.lemma_ in pos_lemmas)
        neg_count = sum(1 for t in doc if t.lemma_ in neg_lemmas)
        
        # Cálculo de Polaridade Híbrida (70% Semântica | 30% Nota do Cliente)
        base_pol = (pos_count - neg_count) / (pos_count + neg_count + 1)
        score_adj = (score - 3) / 2
        polarity = (base_pol * 0.7) + (score_adj * 0.3)

    # Normalização de labels para alinhamento vertical perfeito no console
    if polarity > 0.15:
        label = "POSITIVO 🟢"
    elif polarity < -0.15:
        label = "NEGATIVO 🔴"
    else:
        label = "NEUTRO   🟡" # Espaçamento para alinhar com os labels de 8 caracteres
        
    return round(polarity, 4), label

# ==============================================================================
# 3. PIPELINE PRINCIPAL (DATA QUALITY AUDIT)
# ==============================================================================
def run_pipeline():
    FILE_NAME = 'olist_order_reviews.csv'

    print("\n" + "="*100)
    print("🚀 DADOSFERA PIPELINE: DATA QUALITY AUDIT & ADVANCED NLP")
    print("="*100)

    if not os.path.exists(FILE_NAME):
        print(f"❌ ERRO CRÍTICO: Dataset '{FILE_NAME}' não localizado.")
        return

    # Ingestão para Auditoria
    df = pd.read_csv(FILE_NAME)
    print(f"✅ Ingestão concluída. Registros para análise: {len(df):,}")

    # 🕵️ ITEM 4: DATA QUALITY E OBSERVABILIDADE
    print("\n" + "="*100)
    print("🕵️  RELATÓRIO DE AUDITORIA DE DADOS (DATA CONTRACTS)")
    print("="*100)

    # Check 01: Domínio (review_score)
    print(f"\n[CHECK 01] Consistência de Domínio: 'review_score'")
    min_s, max_s, mean_s = df['review_score'].min(), df['review_score'].max(), df['review_score'].mean()
    errors_dom = df[~df['review_score'].between(1, 5)]
    print(f"    📊 Health Check: Min: {min_s} | Max: {max_s} | Média: {mean_s:.2f}")
    print(f"    ✅ STATUS: {'PASS' if len(errors_dom) == 0 else 'FAIL'}")

    # Check 02: Integridade (review_id)
    print(f"\n[CHECK 02] Integridade Referencial: 'review_id'")
    nulls_id = df['review_id'].isnull().sum()
    print(f"    📊 Registros Nulos: {nulls_id}")
    print(f"    ✅ STATUS: {'PASS' if nulls_id == 0 else 'FAIL'}")

    # 🤖 ITEM 5: ENRIQUECIMENTO DE IA
    print("\n\n" + "="*100)
    print("🤖  PIPELINE DE ENRIQUECIMENTO: NLP FEATURE ENGINEERING")
    print("="*100)
    
    # Amostra para validação visual dos resultados
    sample = df.dropna(subset=['review_comment_message']).head(15).copy()
    
    print(f"{'REVIEW (NLP INPUT)':<75} | {'POLARIDADE':<10} | {'CLASS.'}")
    print("-" * 115)

    for _, row in sample.iterrows():
        pol, lbl = get_sentiment_engine(row['review_comment_message'], row['review_score'])
        txt = " ".join(str(row['review_comment_message']).split())
        display_txt = (txt[:72] + '...') if len(txt) > 72 else txt
        print(f"{display_txt:<75} | {pol:+.4f}   | {lbl:<12}")

    print("-" * 115)
    print(f"✅ Pipeline finalizado com sucesso às {pd.Timestamp.now()}.")

if __name__ == "__main__":
    run_pipeline()
