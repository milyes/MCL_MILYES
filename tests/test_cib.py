import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.cib import generate_payment_form, generate_payment_js_embed

def test_payment_form_has_fields():
    html = generate_payment_form("TestShop", "ORD001", "5000")
    assert "card_number" in html
    assert "card_expiry" in html
    assert "card_cvv" in html
    assert "card_name" in html

def test_payment_form_has_amount():
    html = generate_payment_form("TestShop", "ORD001", "7500")
    assert "7500 DZD" in html

def test_payment_form_has_order_id():
    html = generate_payment_form("TestShop", "ORD123", "5000")
    assert "ORD123" in html

def test_payment_form_has_cib_edahabia():
    html = generate_payment_form("Test", "ORD1", "1000")
    assert "CIB" in html
    assert "Edahabia" in html

def test_payment_form_not_connected():
    html = generate_payment_form("Test", "ORD1", "1000")
    assert "non configuree" in html

def test_payment_js_embed():
    js = generate_payment_js_embed()
    assert "mclPay" in js
    assert "init" in js

def test_payment_form_has_style():
    html = generate_payment_form("Test", "ORD1", "1000")
    assert "border-radius" in html
    assert "#00ff9f" in html

if __name__ == "__main__":
    test_payment_form_has_fields()
    test_payment_form_has_amount()
    test_payment_form_has_order_id()
    test_payment_form_has_cib_edahabia()
    test_payment_form_not_connected()
    test_payment_js_embed()
    test_payment_form_has_style()
    print("test_cib : 7/7 OK")
