"""
Module CIB/Edahabia - v0.3.0-alpha

Ce module genere un formulaire de paiement conforme aux specs CIB.
Il ne traite PAS les paiements (cela requiere un partenaire bancaire).
Il genere uniquement le HTML du formulaire pret a etre connecte.

Conformite : Le formulaire est statique, aucun appel reseau.
La connexion a l'API bancaire doit etre faite par un partenaire certifie.
"""

from datetime import datetime

def generate_payment_form(project_name: str, order_id: str, amount: str) -> str:
    """Genere un formulaire de paiement CIB/Edahabia.

    Args:
        project_name: Nom du projet/merchant
        order_id: ID de commande unique
        amount: Montant en DZD (ex: "5000")

    Returns:
        HTML du formulaire de paiement
    """
    return f'''<section class="payment" id="paiement">
<h2>Paiement securise</h2>
<div class="pay-container">
    <div class="pay-methods">
        <label class="pay-option selected">
            <input type="radio" name="method" value="cib" checked>
            <span class="pay-card cib">CIB</span>
        </label>
        <label class="pay-option">
            <input type="radio" name="method" value="edahabia">
            <span class="pay-card edahabia">Edahabia</span>
        </label>
    </div>
    <form id="paymentForm">
        <input type="hidden" name="merchant" value="{project_name}">
        <input type="hidden" name="order_id" value="{order_id}">
        <input type="hidden" name="amount" value="{amount}">
        <input type="hidden" name="currency" value="DZD">
        <input type="hidden" name="date" value="{datetime.now().isoformat()}">
        <div class="card-fields">
            <input type="text" id="card_number" placeholder="Numéro de carte" maxlength="19" required pattern="[0-9 ]{{13,19}}" autocomplete="cc-number">
            <div class="card-row">
                <input type="text" id="card_expiry" placeholder="MM/AA" maxlength="5" required pattern="[0-9]{{2}}/[0-9]{{2}}" autocomplete="cc-exp">
                <input type="text" id="card_cvv" placeholder="CVV" maxlength="3" required pattern="[0-9]{{3}}" autocomplete="cc-csc">
            </div>
            <input type="text" id="card_name" placeholder="Nom sur la carte" required autocomplete="cc-name">
        </div>
        <div class="pay-summary">
            <div class="pay-line"><span>Total</span><span>{amount} DZD</span></div>
        </div>
        <button type="submit" class="btn pay-btn" style="width:100%">Payer {amount} DZD</button>
        <p class="pay-notice">Paiement securise via CIB/Edahabia. Aucune donnée stockee.</p>
    </form>
</div>
<style>
.payment{{padding:80px 10%;background:#0a1f33;text-align:center}}
.payment h2{{margin-bottom:40px;color:#00ff9f}}
.pay-container{{max-width:480px;margin:0 auto;background:#112b44;padding:40px;border-radius:15px;border:1px solid #1a3a55;text-align:left}}
.pay-methods{{display:flex;gap:12px;margin-bottom:24px}}
.pay-option{{flex:1;cursor:pointer}}
.pay-option input{{display:none}}
.pay-card{{display:block;text-align:center;padding:14px;border-radius:10px;border:2px solid #1a3a55;font-weight:700;font-size:1rem;transition:0.3s}}
.pay-card.cib{{color:#0066cc}}
.pay-card.edahabia{{color:#ff6600}}
.pay-option.selected .pay-card{{border-color:#00ff9f;background:rgba(0,255,159,0.08)}}
.card-fields{{display:flex;flex-direction:column;gap:14px;margin-bottom:20px}}
.card-fields input{{width:100%;padding:14px;border-radius:8px;border:1px solid #1a3a55;background:#0a1f33;color:white;font-size:1rem;box-sizing:border-box}}
.card-fields input:focus{{outline:none;border-color:#00ff9f}}
.card-row{{display:flex;gap:14px}}
.card-row input{{flex:1}}
.pay-summary{{border-top:1px solid #1a3a55;padding-top:16px;margin-bottom:20px}}
.pay-line{{display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700}}
.pay-btn{{margin-top:0}}
.pay-notice{{text-align:center;font-size:0.75rem;color:#5a7a9a;margin-top:16px}}
</style>
<script>
document.querySelectorAll(".pay-option").forEach(function(opt){{
    opt.addEventListener("click",function(){{
        document.querySelectorAll(".pay-option").forEach(function(o){{o.classList.remove("selected")}});
        opt.classList.add("selected");
    }});
}});
document.getElementById("paymentForm").addEventListener("submit",function(e){{
    e.preventDefault();
    var btn=this.querySelector("button");
    btn.innerText="Connexion bancaire en cours...";
    btn.style.background="#1a3a55";btn.style.color="#00ff9f";btn.disabled=true;
    setTimeout(function(){{
        btn.innerText="Connexion bancaire non configuree. V0.3.0-alpha.";
        btn.style.background="rgba(210,16,52,0.2)";btn.style.color="#D21034";
    }},1500);
}});
</script>
</section>'''

def generate_payment_js_embed() -> str:
    """Retourne le JS a inserer dans le template principal pour activer le paiement."""
    return '''
var mclPay = {{
    init: function(orderId, amount) {{
        var sec = document.createElement("div");
        sec.id = "paiement-section";
        document.body.appendChild(sec);
        fetch("/payment-form?order=" + orderId + "&amount=" + amount)
            .then(function(r){{return r.text()}})
            .then(function(html){{sec.innerHTML = html}});
    }}
}};
'''
