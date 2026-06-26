import re
from .ideas import CATEGORIES

KEYWORDS = {
    "food": ["repas","livraison","nourriture","pizza","cafe","the","traiteur","cuisin","restaurant","burger"],
    "tech": ["ia","intelligence","chatbot","code","app","application","traducteur","logiciel","saas","donnees","data"],
    "service": ["marketing","comptabilite","menage","reparation","covoiturage","nettoyage","service","conseil"],
    "ecom": ["vetement","boutique","marketplace","artisanat","cosmetique","goodies","mode","magasin"],
    "immobilier": ["immobilier","location","voiture","demenagement","colocation","coloc","maison","appartement","logement"],
}

def detect_category(idea: str) -> str:
    il = idea.lower()
    for cat, mots in KEYWORDS.items():
        for m in mots:
            if re.search(r"\b" + re.escape(m) + r"\b", il):
                return cat
    return "service"

def get_category_data(category: str) -> dict:
    return CATEGORIES.get(category, CATEGORIES["service"])

def extract_keywords(idea: str) -> list:
    il = idea.lower()
    found = []
    for cat, mots in KEYWORDS.items():
        for m in mots:
            if re.search(r"\b" + re.escape(m) + r"\b", il):
                found.append(m)
    return list(set(found))
