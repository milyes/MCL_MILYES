import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.analyzer import detect_category, get_category_data, extract_keywords

def test_detect_food():
    assert detect_category("Livraison de repas a Alger") == "food"
    assert detect_category("Pizza halal") == "food"
    assert detect_category("traiteur pour mariage") == "food"

def test_detect_tech():
    assert detect_category("IA traducteur Darija") == "tech"
    assert detect_category("chatbot juridique") == "tech"
    assert detect_category("application mobile") == "tech"

def test_detect_service():
    assert detect_category("marketing digital") == "service"
    assert detect_category("comptabilite auto") == "service"

def test_detect_ecom():
    assert detect_category("boutique de vetements") == "ecom"
    assert detect_category("marketplace artisanat") == "ecom"

def test_detect_immobilier():
    assert detect_category("location voiture") == "immobilier"
    assert detect_category("colocation etudiante") == "immobilier"

def test_detect_default():
    assert detect_category("projet quelconque") == "service"
    assert detect_category("xyz") == "service"

def test_get_category_data():
    d = get_category_data("food")
    assert "titre_section" in d
    assert "cards" in d
    assert len(d["cards"]) == 3

def test_get_category_unknown():
    d = get_category_data("inconnu")
    assert d["titre_section"] == "Nos Services"

def test_extract_keywords():
    kw = extract_keywords("livraison de repas a alger")
    assert "livraison" in kw
    assert "repas" in kw

def test_extract_keywords_none():
    kw = extract_keywords("projet xyz")
    assert kw == []

if __name__ == "__main__":
    test_detect_food()
    test_detect_tech()
    test_detect_service()
    test_detect_ecom()
    test_detect_immobilier()
    test_detect_default()
    test_get_category_data()
    test_get_category_unknown()
    test_extract_keywords()
    test_extract_keywords_none()
    print("test_analyzer : 10/10 OK")
