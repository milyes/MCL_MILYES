import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Tuple
from .config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, VERSION
from .analyzer import get_category_data

def generate_html(idea: str, category: str, use_ollama: bool = False) -> Tuple[str, str]:
    idea = idea.replace("<", "&lt;").replace(">", "&gt;")
    idea = idea.replace("<", "&lt;").replace(">", "&gt;")
    if use_ollama:
        h = _ollama(idea)
        if h:
            return h, "ollama_local"
    return _template(idea, category), "template_souverain"

def _ollama(idea: str) -> Optional[str]:
    prompt = (
        "Genere uniquement le code HTML/CSS/JS complet d'un site premium "
        "pour : " + idea + ". Design sombre (#050d14), accents verts (#00ff9f). "
        "Inclus nav, hero, section services avec 3 cartes, formulaire de "
        "contact avec id=\'contactForm\', et footer. Pas de markdown."
    )
    data = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as r:
            res = json.loads(r.read().decode("utf-8"))
            h = res.get("response", "").replace("```html", "").replace("```", "").strip()
            if "<html" in h.lower():
                return h
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        pass
    return None

def _template(idea: str, category: str) -> str:
    cd = get_category_data(category)
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
