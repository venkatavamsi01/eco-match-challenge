# Updated src/core/cleaning.py
import re

# Domain-specific synonyms & generic prefixes
SYNONYMS = {
    "cappuc": "cappuccino",
    "asprgs": "asparagus",
    "toms": "tomatoes",
    # add more abbreviations here
}
GENERIC_PREFIXES = r"\b(?:plant menu|organic|fresh)\b"

# Unit/Quantity pattern
QUANTITY_PATTERN = r"\b\d+(?:\.\d+)?\s?(?:ml|l|g|kg|oz)\b"

def clean_text(text: str) -> str:
    text = text.lower()
    # Apply domain synonyms
    for k, v in SYNONYMS.items():
        text = re.sub(rf"\b{k}\b", v, text)
    # Remove quantities and units
    text = re.sub(QUANTITY_PATTERN, "", text)
    # Strip all-caps brand codes or acronyms
    text = re.sub(r"\b[A-Z]{2,}\b", "", text)
    # Remove ordinals like NO1, trailing numbers
    text = re.sub(r"\bno\d+\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b\d+\b", "", text)
    # Remove generic prefixes
    text = re.sub(GENERIC_PREFIXES, "", text)
    # Normalize non-alphanumeric to spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text