import json
import asyncio
from datetime import datetime
from pathlib import Path
from . import __version__
from .config import PROJECTS_DIR
from .colors import Colors
from .analyzer import detect_category
from .generator import generate_html
from .logo import generate_logo_svg
from .logger import save_log
from .error_handler import get_handler

async def create_startup(idea: str, use_ollama: bool = False, start_server: bool = False) -> dict:
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    pid = f"PROJ_{ts}"
    pf = Path(PROJECTS_DIR) / pid
    pf.mkdir(parents=True, exist_ok=True)
    sf = pf / "index.html"
    logof = pf / "logo.svg"
    leadsf = pf / "leads.json"
    rf = pf / "rapport.json"
    leadsf.write_text("[]", encoding="utf-8")

    print(f"\n{Colors.CYAN}  Projet : {pid}{Colors.RESET}")
    print(f"  Idee   : {idea}\n")

    cat = detect_category(idea)
    print(f"{Colors.YELLOW}  [1/4] Analyse{Colors.RESET} -> Categorie : {cat}")
    await asyncio.sleep(0.2)

    print(f"{Colors.YELLOW}  [2/4] Generation site{Colors.RESET}", end="")
    html, src = get_handler().safe_execute("generator", generate_html, idea, cat, use_ollama)
    if html is None:
        print(f"{Colors.RED}  Generation echouee, fallback template{Colors.RESET}")
        html, src = generate_html(idea, cat, False)
    sf.write_text(html, encoding="utf-8")
    print(f" -> {src} ({len(html)} octets)")
    await asyncio.sleep(0.2)

    print(f"{Colors.YELLOW}  [3/4] Logo{Colors.RESET}", end="")
    lok = get_handler().safe_execute("logo", generate_logo_svg, idea, logof)
    if not lok:
        print(f"{Colors.YELLOW}  Logo: echec, continuation sans logo{Colors.RESET}")
    print(f" -> {'OK' if lok else 'ECHEC'}")
    await asyncio.sleep(0.2)

    print(f"{Colors.YELLOW}  [4/4] Rapport{Colors.RESET}")
    rapport = {
        "project_id": pid, "idea": idea, "category": cat,
        "source_html": src, "logo": "svg_local" if lok else "echec",
        "paiement": "Non implemente - formulaire de contact uniquement",
        "crm": "localStorage + serveur local optionnel",
        "conformite_nsp": "100% stdlib, zero appel reseau etranger",
        "version": __version__, "date": datetime.now().isoformat(),
    }
    rf.write_text(json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")
    save_log({"project_id": pid, "idea": idea, "category": cat, "date": datetime.now().isoformat(), "status": "success", "version": __version__})

    if start_server:
        from .server import serve_leads
        print(f"\n{Colors.MAGENTA}  Serveur leads actif...{Colors.RESET}")
        await serve_leads(str(pf))

    print(f"\n{Colors.GREEN}  Projet cree avec succes.{Colors.RESET}")
    print(f"  Dossier  : {pf}")
    print(f"  Site     : {sf}")
    print(f"  Logo     : {logof}")
    print(f"  Leads    : {leadsf}")
    print(f"  Rapport  : {rf}\n")
    return rapport
