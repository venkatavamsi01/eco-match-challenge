from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def embed_texts(text_list):
    model = get_model()
    return model.encode(text_list, show_progress_bar=True)
