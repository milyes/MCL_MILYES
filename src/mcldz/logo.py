from pathlib import Path

def generate_logo_svg(idea: str, save_path: Path) -> bool:
    mots = [m for m in idea.split() if len(m) > 2][:2]
    txt = "".join(m[0].upper() for m in mots) or "MCL"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#0a1f33"/><stop offset="100%" style="stop-color:#050d14"/></linearGradient><linearGradient id="ac" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00ff9f"/><stop offset="100%" style="stop-color:#00cc7a"/></linearGradient></defs><rect width="512" height="512" rx="80" fill="url(#bg)"/><rect x="16" y="16" width="480" height="480" rx="72" fill="none" stroke="url(#ac)" stroke-width="3" opacity="0.4"/><text x="256" y="290" font-family="Arial,sans-serif" font-size="180" font-weight="bold" fill="url(#ac)" text-anchor="middle">{txt}</text></svg>'''
    try:
        save_path.write_text(svg, encoding="utf-8")
        return True
    except OSError:
        return False
