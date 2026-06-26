#!/usr/bin/env python3
"""NSP-SIG-MCLDZ v0.2.0-alpha — Point d'entree CLI"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import asyncio
from mcldz import __version__
from mcldz.colors import Colors
from mcldz.ideas import IDEES_STARTUPS
from mcldz.security import sanitize_idea
from mcldz.forge import create_startup

async def main():
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}  NSP-SIG-MCLDZ v{__version__}{Colors.RESET}")
    print(f"{Colors.YELLOW}  Forge de Startups Souveraine Algerienne{Colors.RESET}")
    print(f"{Colors.GREEN}  100% stdlib - Zero dependance etrangere{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    print(f"  {Colors.MAGENTA}20 idees de startups par categorie :{Colors.RESET}\n")
    for i, (idea, cat) in enumerate(IDEES_STARTUPS, 1):
        print(f"  {Colors.CYAN}{i:>2}.{Colors.RESET} {idea}  {Colors.YELLOW}[{cat}]{Colors.RESET}")
    print(f"\n  {Colors.BOLD}{'-'*60}{Colors.RESET}")
    choice = input(f"\n  {Colors.CYAN}Choisis un numero (1-20) ou decris ton idee : {Colors.RESET}").strip()
    idea = ""
    if choice.isdigit() and 1 <= int(choice) <= 20:
        idea = IDEES_STARTUPS[int(choice) - 1][0]
        print(f"\n  {Colors.GREEN}Choix : {idea}{Colors.RESET}")
    elif choice:
        try:
            idea = sanitize_idea(choice)
        except ValueError as e:
            print(f"\n  {Colors.RED}Erreur : {e}{Colors.RESET}")
            sys.exit(1)
    else:
        idea = "Boutique en ligne algerienne"
    await create_startup(idea, use_ollama=True)

if __name__ == "__main__":
    asyncio.run(main())
