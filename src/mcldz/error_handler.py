"""
Agent de gestion des erreurs - NSP-SIG-MCLDZ
Capture, classe et reporte les erreurs sans jamais crasher.
"""

import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from .config import DATA_FILE, PROJECTS_DIR
from .logger import save_log


class MCLError:
    """Erreur structuree avec contexte complet."""

    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

    def __init__(self, level: str, module: str, message: str,
                 details: Optional[Dict[str, Any]] = None,
                 exception: Optional[Exception] = None):
        self.level = level.upper()
        self.module = module
        self.message = message
        self.details = details or {}
        self.exception = exception
        self.timestamp = datetime.now().isoformat()
        self.traceback = None
        if exception:
            self.traceback = traceback.format_exc()

    def to_dict(self) -> dict:
        d = {
            "level": self.level,
            "module": self.module,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp,
        }
        if self.traceback:
            d["traceback"] = self.traceback
        return d

    def __str__(self) -> str:
        return f"[{self.level}] {self.module}: {self.message}"


class ErrorHandler:
    """Agent central de gestion des erreurs."""

    def __init__(self, max_history: int = 100):
        self.errors: List[MCLError] = []
        self.max_history = max_history
        self._log_file = Path(PROJECTS_DIR) / "error_log.json"

    def handle(self, level: str, module: str, message: str,
               details: Optional[Dict] = None,
               exception: Optional[Exception] = None) -> MCLError:
        err = MCLError(level, module, message, details, exception)
        self.errors.append(err)

        if len(self.errors) > self.max_history:
            self.errors = self.errors[-self.max_history:]

        # Sauvegarder dans le fichier de log
        try:
            self._save_to_file(err)
        except OSError:
            pass  # Ne jamais crash dans le handler d'erreurs

        # Afficher dans le terminal
        self._print(err)

        return err

    def safe_execute(self, module: str, func, *args, **kwargs) -> Any:
        """Execute une fonction en capturant toute erreur."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle("ERROR", module, str(e), exception=e)
            return None

    def get_stats(self) -> Dict[str, int]:
        """Retourne les statistiques d'erreurs par niveau."""
        stats = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
        for err in self.errors:
            stats[err.level] = stats.get(err.level, 0) + 1
        return stats

    def get_recent(self, count: int = 10) -> List[Dict]:
        """Retourne les N dernieres erreurs."""
        return [e.to_dict() for e in self.errors[-count:]]

    def clear(self) -> None:
        """Vide l'historique des erreurs."""
        self.errors.clear()
        try:
            if self._log_file.exists():
                self._log_file.write_text("[]", encoding="utf-8")
        except OSError:
            pass

    def _save_to_file(self, err: MCLError) -> None:
        logs = []
        if self._log_file.exists():
            try:
                logs = json.loads(self._log_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                logs = []
        logs.append(err.to_dict())
        if len(logs) > self.max_history:
            logs = logs[-self.max_history:]
        self._log_file.parent.mkdir(parents=True, exist_ok=True)
        self._log_file.write_text(
            json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _print(self, err: MCLError) -> None:
        import sys
        from .colors import Colors
        colors = {
            "DEBUG": Colors.CYAN,
            "INFO": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.RED,
        }
        c = colors.get(err.level, Colors.RESET)
        print(f"{c}[{err.level}]{Colors.RESET} {err.module}: {err.message}", file=sys.stderr)


# Instance globale
_handler = None

def get_handler() -> ErrorHandler:
    global _handler
    if _handler is None:
        _handler = ErrorHandler()
    return _handler

def handle_error(level: str, module: str, message: str,
                  details: Optional[Dict] = None,
                  exception: Optional[Exception] = None) -> MCLError:
    """Fonction rapide pour capturer une erreur."""
    return get_handler().handle(level, module, message, details, exception)

def safe_run(module: str, func, *args, **kwargs) -> Any:
    """Fonction rapide pour executer en toute securite."""
    return get_handler().safe_execute(module, func, *args, **kwargs)
