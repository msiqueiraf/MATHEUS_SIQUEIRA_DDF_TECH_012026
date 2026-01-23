import pandas as pd
import spacy
import os

# ==============================================================================
# 1. AMBIENTE E IA (NLP ENGINE)
# ==============================================================================
def load_model():
    """Garante a carga do modelo spaCy no ambiente local do Power BI."""
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        os.system("python -m spacy download pt_core_news_sm")
        return spacy.load("pt_core_news_sm")

nlp = load_model()

def get_sentiment(text, score):
    """Motor de inferência híbrida: NLP + Ground Truth."""
    if pd.isna(text) or str(text).strip() == "":
        polarity = (score - 3) / 2
    else:
        doc = nlp(str(text).lower())
        # Lemmatization avançada para identificação de carga semântica
        pos = sum(1 for t in doc if t.lemma_ in ['bom', 'ótimo', 'excelente', 'rápido', 'recomendo'])
        neg = sum(1 for t in doc if t.lemma_ in ['ruim', 'péssimo', 'atraso', 'lento', 'horrível'])
        
        # Calibração Híbrida: Semântica (70%) e Score (30%)
        base = (pos - neg) / (pos + neg + 1)
        polarity = (base * 0.7) + (((score - 3) / 2) * 0.3)

    label = "POSITIVO" if polarity > 0.15 else "NEGATIVO" if polarity < -0.15 else "NEUTRO"
    return round(polarity, 4), label

# ==============================================================================
# 2. DATA QUALITY E ENRIQUECIMENTO (POWER QUERY EXECUTION)
# ==============================================================================

# ITEM 4: Observabilidade de Dados (Checks transformados em métricas de BI)
dataset['DQ_Score_Check'] = dataset['review_score'].apply(lambda x: 'PASS' if 1 <= x <= 5 else 'FAIL')
dataset['DQ_ID_Check'] = dataset['review_id'].apply(lambda x: 'PASS' if pd.notnull(x) else 'FAIL')

# ITEM 5: NLP Feature Engineering
sentiment_data = dataset.apply(
    lambda r: get_sentiment(r['review_comment_message'], r['review_score']), axis=1
)

# Desmembramento dos resultados em colunas estruturadas
dataset[['Polaridade_IA', 'Sentimento_IA']] = pd.DataFrame(sentiment_data.tolist(), index=dataset.index)
