import re
from .config import MAX_IDEA_LENGTH, SAFE_FILENAME_RE

def sanitize_idea(idea: str) -> str:
    idea = idea.strip()
    if not idea:
        raise ValueError("L'idee ne peut pas etre vide.")
    if len(idea) > MAX_IDEA_LENGTH:
        raise ValueError(f"L'idee ne peut pas depasser {MAX_IDEA_LENGTH} caracteres.")
    idea = idea.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return idea

def safe_filename(idea: str) -> str:
    cleaned = re.sub(SAFE_FILENAME_RE, "", idea)
    return cleaned[:60].strip().replace(" ", "_") or "projet"

def validate_phone(phone: str) -> bool:
    p = phone.strip().replace(" ", "").replace("-", "")
    return bool(re.match(r"^0[5-7][0-9]{8}$", p))
