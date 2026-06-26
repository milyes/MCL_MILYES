# Changelog NSP-SIG-MCLDZ

## [0.2.0-alpha] - 2024

### Ajoute
- Decomposition en modules (src/mcldz/)
  - config.py : configuration centralisee
  - colors.py : couleurs terminal
  - ideas.py : idees et categories
  - security.py : sanitisation + validation telephone
  - analyzer.py : detection categorie + extraction mots-cles
  - generator.py : generation HTML (ollama + template)
  - logo.py : generation logo SVG
  - server.py : serveur leads asyncio
  - forge.py : orchestrateur
  - cib.py : formulaire CIB/Edahabia (premier jet)
- 48 tests unitaires (security/analyzer/generator/logger/logo/cib)
- Script run_tests.sh
- validate_phone() : validation numeros algeriens

### Change
- AI_AUTO.py reduit a 40 lignes (CLI mince)
- Toute la logique dans src/mcldz/

### Securite
- Validation format telephone algerien (05xx/06xx/07xx)
- Tests XSS sur le template

## [0.1.0-alpha] - 2024

### Ajoute
- Refactorisation initiale
- 5 categories adaptees
- Logo SVG local
- Mini serveur leads
- Sanitisation inputs
- .gitignore + docs

### Supprime
- IA_AUTO_UPDATE.py
- AI_AUTO_distante.py
- Pollinations.ai
- Fausse revendication CIB
