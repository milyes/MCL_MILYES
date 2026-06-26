import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.security import sanitize_idea, safe_filename, validate_phone

def test_sanitize_normal():
    assert sanitize_idea("Livraison de repas") == "Livraison de repas"

def test_sanitize_empty():
    try:
        sanitize_idea("")
        assert False, "Should raise"
    except ValueError:
        pass

def test_sanitize_too_long():
    try:
        sanitize_idea("x" * 501)
        assert False, "Should raise"
    except ValueError:
        pass

def test_sanitize_html():
    assert "<script>" not in sanitize_idea("<script>alert(1)</script>")
    assert "&lt;" in sanitize_idea("<test>")

def test_sanitize_quotes():
    r = sanitize_idea('test "quote"')
    assert "\"" not in r or "&quot;" in r

def test_safe_filename_normal():
    assert safe_filename("Mon super projet") == "Mon_super_projet"

def test_safe_filename_special():
    assert "test" in safe_filename("test@#$%^&*()")

def test_safe_filename_empty():
    assert safe_filename("!!!") == "projet"

def test_validate_phone_valid():
    assert validate_phone("0555123456") == True
    assert validate_phone("0777890123") == True
    assert validate_phone("0666123456") == True

def test_validate_phone_invalid():
    assert validate_phone("123456789") == False
    assert validate_phone("05551234567") == False
    assert validate_phone("abcdefghij") == False
    assert validate_phone("") == False

def test_validate_phone_spaces():
    assert validate_phone("0555 123 456") == True
    assert validate_phone("0555-123-456") == True

if __name__ == "__main__":
    test_sanitize_normal()
    test_sanitize_empty()
    test_sanitize_too_long()
    test_sanitize_html()
    test_sanitize_quotes()
    test_safe_filename_normal()
    test_safe_filename_special()
    test_safe_filename_empty()
    test_validate_phone_valid()
    test_validate_phone_invalid()
    test_validate_phone_spaces()
    print("test_security : 11/11 OK")
