import json
from pathlib import Path
from .config import DATA_FILE

def _get_data_file() -> Path:
    from . import config as cfg
    return Path(cfg.DATA_FILE)

def load_logs() -> list:
    try:
        p = _get_data_file()
        if p.exists():
            c = p.read_text(encoding="utf-8").strip()
            if c:
                return json.loads(c)
    except (json.JSONDecodeError, OSError):
        pass
    return []

def save_log(entry: dict) -> None:
    logs = load_logs()
    logs.append(entry)
    _get_data_file().write_text(
        json.dumps(logs, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def load_project_leads(project_dir: str) -> list:
    p = Path(project_dir) / "leads.json"
    try:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        pass
    return []

def save_lead(project_dir: str, lead: dict) -> bool:
    p = Path(project_dir) / "leads.json"
    try:
        leads = load_project_leads(project_dir)
        leads.append(lead)
        p.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except OSError:
        return False
