import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\b(?:organic|brand|fresh|pack|pkg)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
