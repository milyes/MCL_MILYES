import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.logo import generate_logo_svg
from pathlib import Path

def test_logo_created():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "logo.svg"
        assert generate_logo_svg("Mon super projet", p) == True
        assert p.exists()

def test_logo_is_svg():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "logo.svg"
        generate_logo_svg("Test projet", p)
        content = p.read_text()
        assert "<svg" in content
        assert "</svg>" in content

def test_logo_has_initials():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "logo.svg"
        generate_logo_svg("Boutique Algerie", p)
        content = p.read_text()
        assert "BA" in content

def test_logo_short_idea():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "logo.svg"
        generate_logo_svg("OK", p)
        content = p.read_text()
        assert "MCL" in content

def test_logo_has_gradient():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "logo.svg"
        generate_logo_svg("Test", p)
        content = p.read_text()
        assert "linearGradient" in content
        assert "#00ff9f" in content

if __name__ == "__main__":
    test_logo_created()
    test_logo_is_svg()
    test_logo_has_initials()
    test_logo_short_idea()
    test_logo_has_gradient()
    print("test_logo : 5/5 OK")
