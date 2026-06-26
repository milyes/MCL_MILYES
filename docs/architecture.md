# Architecture NSP-SIG-MCLDZ v0.1.0-alpha

## Flux
Utilisateur -> CLI -> sanitize_idea() -> detect_category() -> create_startup()
  -> generate_html() -> _ollama() ou _template()
  -> generate_logo_svg() -> save_log() -> rapport.json

## Appels reseaux
| Destination | Port | Souverain |
|localhost:11434| 11434 | OUI (Ollama) |
| localhost:8080| 8080 | OUI (leads) |

## Dependances
100% stdlib : asyncio, json, urllib, pathlib, re, datetime, typing
