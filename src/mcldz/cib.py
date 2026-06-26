"""
Module CIB/Edahabia - NSP-SIG-MCLDZ
Formulaire de paiement statique. Aucun appel reseau.
"""

from datetime import datetime

def generate_payment_form(project_name, order_id, amount):
    return (
        '<section class="payment" id="paiement">'
        '<h2>Paiement securise</h2>'
        '<div class="pay-container">'
        '<div class="pay-methods">'
        '<label class="pay-option selected">'
        '<input type="radio" name="method" value="cib" checked>'
        '<span class="pay-card cib">CIB</span>'
        '</label>'
        '<label class="pay-option">'
        '<input type="radio" name="method" value="edahabia">'
        '<span class="pay-card edahabia">Edahabia</span>'
        '</label>'
        '</div>'
        '<form id="paymentForm">'
        '<input type="hidden" name="merchant" value="' + str(project_name) + '">'
        '<input type="hidden" name="order_id" value="' + str(order_id) + '">'
        '<input type="hidden" name="amount" value="' + str(amount) + '">'
        '<input type="hidden" name="currency" value="DZD">'
        '<input type="hidden" name="date" value="' + datetime.now().isoformat() + '">'
        '<div class="card-fields">'
        '<input type="text" id="card_number" placeholder="Numero de carte" maxlength="19" required>'
        '<div class="card-row">'
        '<input type="text" id="card_expiry" placeholder="MM/AA" maxlength="5" required>'
        '<input type="text" id="card_cvv" placeholder="CVV" maxlength="3" required>'
        '</div>'
        '<input type="text" id="card_name" placeholder="Nom sur la carte" required>'
        '</div>'
        '<div class="pay-summary">'
        '<div class="pay-line"><span>Total</span><span>' + str(amount) + ' DZD</span></div>'
        '</div>'
        '<button type="submit" class="btn pay-btn" style="width:100%">Payer ' + str(amount) + ' DZD</button>'
        '<p class="pay-notice">Paiement securise via CIB/Edahabia.</p>'
        '</form>'
        '</div>'
        '<style>'
        '.payment{padding:80px 10%;background:#0a1f33;text-align:center}'
        '.payment h2{margin-bottom:40px;color:#00ff9f}'
        '.pay-container{max-width:480px;margin:0 auto;background:#112b44;padding:40px;border-radius:15px;border:1px solid #1a3a55;text-align:left}'
        '.pay-methods{display:flex;gap:12px;margin-bottom:24px}'
        '.pay-option{flex:1;cursor:pointer}'
        '.pay-option input{display:none}'
        '.pay-card{display:block;text-align:center;padding:14px;border-radius:10px;border:2px solid #1a3a55;font-weight:700;font-size:1rem;transition:0.3s}'
        '.pay-card.cib{color:#0066cc}'
        '.pay-card.edahabia{color:#ff6600}'
        '.pay-option.selected .pay-card{border-color:#00ff9f;background:rgba(0,255,159,0.08)}'
        '.card-fields{display:flex;flex-direction:column;gap:14px;margin-bottom:20px}'
        '.card-fields input{width:100%;padding:14px;border-radius:8px;border:1px solid #1a3a55;background:#0a1f33;color:white;font-size:1rem;box-sizing:border-box}'
        '.card-fields input:focus{outline:none;border-color:#00ff9f}'
        '.card-row{display:flex;gap:14px}'
        '.card-row input{flex:1}'
        '.pay-summary{border-top:1px solid #1a3a55;padding-top:16px;margin-bottom:20px}'
        '.pay-line{display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700}'
        '.pay-notice{text-align:center;font-size:0.75rem;color:#5a7a9a;margin-top:16px}'
        '</style>'
        '<script>'
        'document.querySelectorAll(".pay-option").forEach(function(o){o.addEventListener("click",function(){document.querySelectorAll(".pay-option").forEach(function(x){x.classList.remove("selected")});o.classList.add("selected")})});'
        'document.getElementById("paymentForm").addEventListener("submit",function(e){'
        'e.preventDefault();'
        'var b=this.querySelector("button");'
        'b.innerText="Traitement en cours...";'
        'b.style.background="#1a3a55";b.style.color="#00ff9f";b.disabled=true;'
        'setTimeout(function(){'
        'var n=document.querySelector(".pay-notice");'
        'n.innerText="Simulation OK - "+b.getAttribute("data-order")+" - "+b.getAttribute("data-amount")+" DZD";'
        'n.style.color="#00ff9f";'
        'b.innerText="Paiement simule avec succes";'
        'b.style.background="rgba(0,204,85,0.15)";'
        '},2500)'
        '})'
        '</script>'
        '</section>'
    )

def generate_payment_js_embed():
    return (
        "var mclPay = {"
        "init: function(orderId, amount) {"
        "  var s = document.createElement('div');"
        "  s.id = 'paiement-section';"
        "  document.body.appendChild(s);"
        "  fetch('/payment-form?order=' + orderId + '&amount=' + amount)"
        "    .then(function(r){return r.text()})"
        "    .then(function(h){s.innerHTML = h});"
        "}"
        "};"
    )
