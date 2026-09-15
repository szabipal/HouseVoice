import re
import unicodedata


def normalize_food_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9 ]+", " ", text).lower()
    return re.sub(r"\s+", " ", text).strip()
