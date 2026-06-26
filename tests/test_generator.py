import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.generator import generate_html, _template

def test_template_returns_html():
    html, src = generate_html("Test projet", "food", use_ollama=False)
    assert "<!DOCTYPE html>" in html
    assert "Test projet" in html
    assert src == "template_souverain"

def test_template_has_form():
    html, _ = generate_html("Test", "tech")
    assert "contactForm" in html
    assert "name" in html
    assert "phone" in html

def test_template_has_nav():
    html, _ = generate_html("Test", "service")
    assert "<nav>" in html
    assert "Accueil" in html

def test_template_has_footer():
    html, _ = generate_html("Test", "ecom")
    assert "<footer>" in html
    assert "NSP-SIG-MCLDZ" in html

def test_template_food_cards():
    html, _ = generate_html("Resto", "food")
    assert "Livraison Rapide" in html
    assert "Cuisine Authentique" in html

def test_template_tech_cards():
    html, _ = generate_html("App", "tech")
    assert "IA Locale" in html
    assert "Securise" in html

def test_template_ollama_false():
    html, src = generate_html("Test", "food", use_ollama=False)
    assert src == "template_souverain"

def test_template_ollama_true_no_server():
    html, src = generate_html("Test", "food", use_ollama=True)
    assert src == "template_souverain"
    assert "<!DOCTYPE html>" in html

def test_template_xss_safe():
    html, _ = generate_html("<script>alert(1)</script>", "food")
    assert "&lt;script&gt;" in html
    assert "<script>alert(1)</script>" not in html

def test_template_size():
    html, _ = generate_html("Mon super projet de test", "service")
    assert len(html) > 1000

if __name__ == "__main__":
    test_template_returns_html()
    test_template_has_form()
    test_template_has_nav()
    test_template_has_footer()
    test_template_food_cards()
    test_template_tech_cards()
    test_template_ollama_false()
    test_template_ollama_true_no_server()
    test_template_xss_safe()
    test_template_size()
    print("test_generator : 10/10 OK")
