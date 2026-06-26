# Securite NSP-SIG-MCLDZ

## Menaces mitigees
- Execution code distant : IA_AUTO_UPDATE.py supprime
- Injection donnees : inputs sanitises, 500 char max
- Dependances etrangeres : zero dependance pip
- Interception leads : serveur sur 127.0.0.1 uniquement

## Pour la production
1. HTTPS devant le serveur leads (nginx + certbot)
2. Chiffrer leads.json au repos
3. Rate limiter sur /save-lead
4. Valider format numero telephone
5. Politique retention donnees (Loi 18-05)
