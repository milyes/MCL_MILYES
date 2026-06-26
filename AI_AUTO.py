#!/usr/bin/env python3
# VERSION: 0.1.0-alpha
# NSP-SIG-MCLDZ - Forge de Startups Souveraine Algerienne
# 100% stdlib - Zero dependance etrangere - Zero appel reseau non souverain

import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

VERSION = "0.1.0-alpha"
PRODUCT = "NSP-SIG-MCLDZ"
DATA_FILE = Path("mcl_milyes_logs.json")
PROJECTS_DIR = Path("projects")
MAX_IDEA_LENGTH = 500
SAFE_FILENAME_RE = re.compile(r"[^a-zA-Z0-9_\-\s]")

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"

if not sys.stdout.isatty():
    for a in vars(Colors):
        if not a.startswith("_") and a != "RESET":
            setattr(Colors, a, "")

IDEES_STARTUPS = [
    ("Livraison repas algeriens avec CIB", "food"),
    ("Epicerie locale livree en 30 min", "food"),
    ("Service de traiteur pour mariages", "food"),
    ("Commande de cafes/the sur demande", "food"),
    ("IA traducteur Darija/Francais/Anglais", "tech"),
    ("Chatbot juridique pour startups", "tech"),
    ("Gestion de stock pour petits commerces", "tech"),
    ("Apprentissage du code en Darija", "tech"),
    ("Covoiturage inter-wilayas", "service"),
    ("Menage et reparations a domicile", "service"),
    ("Comptabilite auto pour micro-entreprises", "service"),
    ("Agence de marketing digital 100% DZ", "service"),
    ("Vetements traditionnels algeriens", "ecom"),
    ("Marketplace d'artisanat local", "ecom"),
    ("Cosmetiques naturels (ghassoul, argile)", "ecom"),
    ("Personnalisation de goodies et imprimes", "ecom"),
    ("Location de voitures entre particuliers", "immobilier"),
    ("Agence immobilere avec visites 3D", "immobilier"),
    ("Demenagement collaboratif", "immobilier"),
    ("Colocation etudiante securisee", "immobilier"),
]

CATEGORIES = {
    "food": {
        "titre_section": "Nos Plats & Services",
        "cards": [
            ("Livraison Rapide", "Vos commandes en 30 min maximum."),
            ("Cuisine Authentique", "Recettes traditionnelles algeriennes."),
            ("Paiement CIB", "Reglez facilement avec votre carte."),
        ],
    },
    "tech": {
        "titre_section": "Nos Solutions Tech",
        "cards": [
            ("IA Locale", "Intelligence artificielle souveraine."),
            ("Securise", "Vos donnees restent en Algerie."),
            ("Performant", "Optimise pour les connexions locales."),
        ],
    },
    "service": {
        "titre_section": "Nos Services",
        "cards": [
            ("Sur Mesure", "Solutions adaptees a votre besoin."),
            ("Accompagnement", "Suivi personnalise en Darija."),
            ("Reporting", "Tableaux de bord en temps reel."),
        ],
    },
    "ecom": {
        "titre_section": "Nos Produits",
        "cards": [
            ("Stock Local", "Produits disponibles en Algerie."),
            ("Personnalisation", "Gravure et customisation."),
            ("Livraison Wilayas", "Expedition vers toutes les wilayas."),
        ],
    },
    "immobilier": {
        "titre_section": "Nos Offres",
        "cards": [
            ("Verifie", "Chaque annonce est controlee."),
            ("Geolocalisation", "Recherche par wilaya et commune."),
            ("Contact Direct", "Mise en relation immediate."),
        ],
    },
}

def load_logs():
    try:
        if DATA_FILE.exists():
            c = DATA_FILE.read_text(encoding="utf-8").strip()
            if c:
                return json.loads(c)
    except (json.JSONDecodeError, OSError):
        pass
    return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    DATA_FILE.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")

def sanitize_idea(idea):
    idea = idea.strip()
    if not idea:
        raise ValueError("L'idee ne peut pas etre vide.")
    if len(idea) > MAX_IDEA_LENGTH:
        raise ValueError(f"L'idee ne peut pas depasser {MAX_IDEA_LENGTH} caracteres.")
    idea = idea.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return idea

def safe_filename(idea):
    c = SAFE_FILENAME_RE.sub("", idea)
    return c[:60].strip().replace(" ", "_") or "projet"

def detect_category(idea):
    il = idea.lower()
    kw = {
        "food": ["repas","livraison","nourriture","pizza","cafe","the","traiteur","cuisin","restaurant","burger"],
        "tech": ["ia","intelligence","chatbot","code","app","application","traducteur","logiciel","saas","donnees","data"],
        "service": ["marketing","comptabilite","menage","reparation","covoiturage","nettoyage","service","conseil"],
        "ecom": ["vetement","boutique","marketplace","artisanat","cosmetique","goodies","mode","magasin"],
        "immobilier": ["immobilier","location","voiture","demenagement","colocation","maison","appartement"],
    }
    for cat, mots in kw.items():
        if any(m in il for m in mots):
            return cat
    return "service"

def generate_html(idea, category, use_ollama=False):
    if use_ollama:
        h = _ollama(idea)
        if h:
            return h, "ollama_local"
    return _template(idea, category), "template_souverain"

def _ollama(idea):
    import urllib.request
    import urllib.error
    prompt = (
        "Genere uniquement le code HTML/CSS/JS complet d'un site premium "
        "pour : " + idea + ". Design sombre (#050d14), accents verts (#00ff9f). "
        "Inclus nav, hero, section services avec 3 cartes, formulaire de "
        "contact avec id=\'contactForm\', et footer. Pas de markdown."
    )
    data = json.dumps({"model":"llama3","prompt":prompt,"stream":False}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode("utf-8"))
            h = res.get("response","").replace("```html","").replace("```","").strip()
            if "<html" in h.lower():
                return h
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        pass
    print(f"{Colors.RED}  Ollama indisponible. Template souverain active.{Colors.RESET}")
    return None

def _template(idea, category):
    cd = CATEGORIES.get(category, CATEGORIES["service"])
    cards = ""
    for t, d in cd["cards"]:
        cards += '            <div class="card"><h3>' + t + '</h3><p>' + d + '</p></div>\n'
    logo = '<img src="logo.svg" alt="Logo" class="logo" onerror="this.style.display=\'none\'">'
    word = idea.split()[0] if idea.split() else "Startup"
    yr = datetime.now().year
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="generator" content="NSP-SIG-MCLDZ/{VERSION}">
<title>{idea}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:\'Segoe UI\',Tahoma,Geneva,Verdana,sans-serif}}
body{{background:#050d14;color:#fff;line-height:1.6}}
nav{{display:flex;justify-content:space-between;align-items:center;padding:20px 10%;background:rgba(10,31,51,0.9);backdrop-filter:blur(10px);position:fixed;width:100%;top:0;z-index:1000;border-bottom:1px solid #112b44}}
nav .logo-text{{font-size:1.5rem;color:#00ff9f;font-weight:bold}}
nav ul{{list-style:none;display:flex;gap:20px}}
nav ul li a{{color:#fff;text-decoration:none;transition:0.3s}}
nav ul li a:hover{{color:#00ff9f}}
.hero{{height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:radial-gradient(circle at top right,#112b44,#050d14);padding:0 20px}}
.hero .logo{{width:150px;height:150px;border-radius:50%;border:4px solid #00ff9f;margin-bottom:30px;box-shadow:0 0 30px rgba(0,255,159,0.3);object-fit:cover}}
.hero h1{{font-size:3.5rem;color:#00ff9f;margin-bottom:20px;text-transform:uppercase;letter-spacing:2px}}
.hero p{{font-size:1.2rem;color:#a0c4e8;max-width:600px;margin-bottom:40px}}
.btn{{background:linear-gradient(45deg,#00ff9f,#00cc7a);color:#050d14;padding:18px 45px;border-radius:50px;font-size:1.2rem;font-weight:bold;text-decoration:none;display:inline-block;transition:transform 0.3s,box-shadow 0.3s;border:none;cursor:pointer}}
.btn:hover{{transform:translateY(-5px);box-shadow:0 10px 20px rgba(0,255,159,0.4)}}
.features{{padding:100px 10%;background:#0a1f33}}
.features h2{{text-align:center;font-size:2.5rem;margin-bottom:50px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:30px}}
.card{{background:#112b44;padding:30px;border-radius:15px;text-align:center;border:1px solid #1a3a55;transition:0.3s}}
.card:hover{{transform:translateY(-10px);border-color:#00ff9f;box-shadow:0 10px 20px rgba(0,0,0,0.3)}}
.card h3{{color:#00ff9f;margin-bottom:15px}}
.contact{{padding:80px 10%;background:#050d14;text-align:center}}
.contact h2{{margin-bottom:40px;color:#00ff9f}}
.form-container{{max-width:500px;margin:0 auto;background:#112b44;padding:40px;border-radius:15px;border:1px solid #1a3a55}}
input,textarea{{width:100%;padding:15px;margin-bottom:20px;border-radius:8px;border:1px solid #1a3a55;background:#0a1f33;color:white;font-size:1rem}}
input:focus,textarea:focus{{outline:none;border-color:#00ff9f}}
textarea{{height:100px;resize:none}}
footer{{text-align:center;padding:30px;background:#050d14;color:#5a7a9a;border-top:1px solid #112b44}}
@media(max-width:768px){{nav ul{{display:none}}.hero h1{{font-size:2.2rem}}}}
</style>
</head>
<body>
<nav><div class="logo-text">{word}</div><ul><li><a href="#accueil">Accueil</a></li><li><a href="#services">Services</a></li><li><a href="#contact">Contact</a></li></ul></nav>
<section class="hero" id="accueil">{logo}<h1>{idea}</h1><p>Solution 100% algerienne, concue par NSP-SIG-MCLDZ.</p><a href="#contact" class="btn">Demarrer votre projet</a></section>
<section class="features" id="services"><h2>{cd["titre_section"]}</h2><div class="grid">{cards}</div></section>
<section class="contact" id="contact"><h2>Demarrer votre projet</h2><div class="form-container"><form id="contactForm"><input type="text" id="name" placeholder="Votre nom complet" required><input type="tel" id="phone" placeholder="Telephone (0555XXXXXX)" required><textarea id="message" placeholder="Decrivez votre besoin..."></textarea><button type="submit" class="btn" style="width:100%">Envoyer ma demande</button></form></div></section>
<footer><p>&copy; {yr} {idea} | Propulse par <strong style="color:#00ff9f">NSP-SIG-MCLDZ</strong></p></footer>
<script>
document.getElementById("contactForm").addEventListener("submit",function(e){{e.preventDefault();var l={{name:document.getElementById("name").value,phone:document.getElementById("phone").value,message:document.getElementById("message").value,date:new Date().toISOString()}};var ls=JSON.parse(localStorage.getItem("mcldz_leads")||"[]");ls.push(l);localStorage.setItem("mcldz_leads",JSON.stringify(ls));var b=this.querySelector("button");b.innerText="Merci ! Nous vous recontacterons.";b.style.background="#1a3a55";b.style.color="#00ff9f";b.disabled=true}});
</script>
</body></html>'''

def generate_logo_svg(idea, save_path):
    mots = [m for m in idea.split() if len(m) > 2][:2]
    txt = "".join(m[0].upper() for m in mots) or "MCL"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#0a1f33"/><stop offset="100%" style="stop-color:#050d14"/></linearGradient><linearGradient id="ac" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00ff9f"/><stop offset="100%" style="stop-color:#00cc7a"/></linearGradient></defs><rect width="512" height="512" rx="80" fill="url(#bg)"/><rect x="16" y="16" width="480" height="480" rx="72" fill="none" stroke="url(#ac)" stroke-width="3" opacity="0.4"/><text x="256" y="290" font-family="Arial,sans-serif" font-size="180" font-weight="bold" fill="url(#ac)" text-anchor="middle">{txt}</text></svg>'''
    try:
        save_path.write_text(svg, encoding="utf-8")
        return True
    except OSError:
        return False

async def serve_leads(project_dir, port=8080):
    lf = project_dir / "leads.json"
    async def handler(reader, writer):
        rl = (await reader.readline()).decode("utf-8", errors="replace")
        parts = rl.split(" ", 2)
        if len(parts) < 2:
            writer.close()
            return
        method, path = parts[0], parts[1]
        if method == "POST" and path == "/save-lead":
            body = b""
            while True:
                chunk = await reader.read(1024)
                if not chunk:
                    break
                body += chunk
                if len(body) > 10000:
                    break
            try:
                lead = json.loads(body.decode("utf-8"))
                leads = []
                if lf.exists():
                    leads = json.loads(lf.read_text(encoding="utf-8"))
                leads.append(lead)
                lf.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
                resp, st = '{"status":"ok"}', "200 OK"
            except (json.JSONDecodeError, OSError):
                resp, st = '{"status":"error"}', "400 Bad Request"
        elif method == "GET" and path == "/leads":
            resp = lf.read_text(encoding="utf-8") if lf.exists() else "[]"
            st = "200 OK"
        else:
            resp, st = '{"status":"not_found"}', "404 Not Found"
        writer.write(f"HTTP/1.1 {st}\r\n".encode())
        writer.write(b"Content-Type: application/json\r\n")
        writer.write(b"Access-Control-Allow-Origin: *\r\n")
        writer.write(f"Content-Length: {len(resp)}\r\n".encode())
        writer.write(b"\r\n")
        writer.write(resp.encode())
        await writer.drain()
        writer.close()
    server = await asyncio.start_server(handler, "127.0.0.1", port)
    print(f"{Colors.GREEN}  Serveur leads : http://127.0.0.1:{port}{Colors.RESET}")
    async with server:
        await server.serve_forever()

async def create_startup(idea, use_ollama=False, start_server=False):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    pid = f"PROJ_{ts}"
    pf = PROJECTS_DIR / pid
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
    await asyncio.sleep(0.3)
    print(f"{Colors.YELLOW}  [2/4] Generation site{Colors.RESET}", end="")
    html, src = generate_html(idea, cat, use_ollama)
    sf.write_text(html, encoding="utf-8")
    print(f" -> {src} ({len(html)} octets)")
    await asyncio.sleep(0.3)
    print(f"{Colors.YELLOW}  [3/4] Logo{Colors.RESET}", end="")
    lok = generate_logo_svg(idea, logof)
    print(f" -> {'OK' if lok else 'ECHEC'}")
    await asyncio.sleep(0.3)
    print(f"{Colors.YELLOW}  [4/4] Rapport{Colors.RESET}")
    rapport = {
        "project_id": pid, "idea": idea, "category": cat,
        "source_html": src, "logo": "svg_local" if lok else "echec",
        "paiement": "Non implemente - formulaire de contact uniquement",
        "crm": "localStorage + serveur local optionnel",
        "conformite_nsp": "100% stdlib, zero appel reseau etranger",
        "version": VERSION, "date": datetime.now().isoformat(),
    }
    rf.write_text(json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")
    save_log({"project_id": pid, "idea": idea, "category": cat, "date": datetime.now().isoformat(), "status": "success", "version": VERSION})
    if start_server:
        print(f"\n{Colors.MAGENTA}  Serveur leads actif...{Colors.RESET}")
        await serve_leads(pf)
    print(f"\n{Colors.GREEN}  Projet cree avec succes.{Colors.RESET}")
    print(f"  Dossier  : {pf}")
    print(f"  Site     : {sf}")
    print(f"  Logo     : {logof}")
    print(f"  Leads    : {leadsf}")
    print(f"  Rapport  : {rf}\n")
    return rapport

async def main():
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}  NSP-SIG-MCLDZ v{VERSION}{Colors.RESET}")
    print(f"{Colors.YELLOW}  Forge de Startups Souveraine Algerienne{Colors.RESET}")
    print(f"{Colors.GREEN}  100% stdlib - Zero dependance etrangere{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    print(f"  {Colors.MAGENTA}20 idees de startups par categorie :{Colors.RESET}\n")
    for i, (idea, cat) in enumerate(IDEES_STARTUPS, 1):
        print(f"  {Colors.CYAN}{i:>2}.{Colors.RESET} {idea}  {Colors.YELLOW}[{cat}]{Colors.RESET}")
    print(f"\n  {Colors.BOLD}{'-'*60}{Colors.RESET}")
    choice = input(f"\n  {Colors.CYAN}Choisis un numero (1-20) ou decris ton idee : {Colors.RESET}").strip()
    idea = ""
    if choice.isdigit() and 1 <= int(choice) <= 20:
        idea = IDEES_STARTUPS[int(choice) - 1][0]
        print(f"\n  {Colors.GREEN}Choix : {idea}{Colors.RESET}")
    elif choice:
        try:
            idea = sanitize_idea(choice)
        except ValueError as e:
            print(f"\n  {Colors.RED}Erreur : {e}{Colors.RESET}")
            sys.exit(1)
    else:
        idea = "Boutique en ligne algerienne"
    await create_startup(idea, use_ollama=True)

if __name__ == "__main__":
    asyncio.run(main())
