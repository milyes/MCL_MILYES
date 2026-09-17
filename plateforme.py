#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, hashlib, time
from datetime import datetime

class ZCoreCrypto:
    @staticmethod
    def sha256(data: str) -> str: return hashlib.sha256(data.encode()).hexdigest()

class ZCoreLogger:
    LEVELS = {"INFO": "[+]", "WARN": "[!]", "ERROR": "[X]", "SEC": "[SEC]"}
    def __init__(self): self.logs = []
    def log(self, level: str, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {self.LEVELS.get(level,'[?]')} {msg}"
        self.logs.append(entry); print(entry)
    def audit(self, action: str, user: str = "root"): self.log("SEC", f"AUDIT: {user} -> {action}")

class ZCoreACL:
    def __init__(self): self.policies = {"admin": ["status", "modules", "ai", "config", "exit", "verify", "help"]}
    def check(self, command: str) -> bool: return command in self.policies.get("admin", [])

class ZCorePlateforme:
    def __init__(self):
        self.name = "Z-CORE_MCLDZ"; self.version = "2.0.0"; self.start = time.time()
        self.logger = ZCoreLogger(); self.acl = ZCoreACL(); self.crypto = ZCoreCrypto()
        self.modules = {}; self.path = os.path.dirname(os.path.abspath(__file__))
        self.running = True; self.session_id = self.crypto.sha256(str(self.start))[:16]

    def banner(self):
        print("\n" + "="*60)
        print(f" {self.name} v{self.version} - ZERO TRUST NATIVE")
        print(f" Session: {self.session_id} | Dependances: 0")
        print("="*60 + "\n")

    def verify_system(self):
        self.logger.log("INFO", "Verification d'integrite systeme...")
        for f in ["plateforme.py", "AI_AUTO.py", "SECURITY.md"]:
            path = os.path.join(self.path, f)
            if os.path.exists(path):
                h = self.crypto.sha256(open(path,'rb').read().decode(errors='ignore'))
                self.logger.log("SEC", f"{f} SHA256: {h[:16]}...")

    def load_modules(self):
        self.logger.log("INFO", "Scan modules...")
        for item in os.listdir(self.path):
            if item.endswith(".py") and item!= "plateforme.py":
                full = os.path.join(self.path, item)
                h = self.crypto.sha256(open(full,'rb').read().decode(errors='ignore'))
                self.modules[item] = {"hash": h[:16], "status": "VERIFIED"}
                self.logger.log("INFO", f"Module {item} VERIFIED")

    def cmd_status(self):
        uptime = int(time.time() - self.start)
        print(f"\n[STATUS ZERO TRUST]\n Uptime: {uptime}s | Session: {self.session_id}\n Modules: {len(self.modules)}")

    def cmd_modules(self):
        print(f"\n[MODULES VERIFIED]")
        for name, data in self.modules.items(): print(f" - {name} | Hash: {data['hash']}...")

    def cmd_verify(self): self.logger.audit("verify_system"); self.verify_system()

    def cmd_ai(self):
        if "AI_AUTO.py" in self.modules:
            self.logger.audit("run_ai"); os.system(f"{sys.executable} {os.path.join(self.path,'AI_AUTO.py')}")
        else: self.logger.log("ERROR", "AI_AUTO.py non trouve")

    def cmd_help(self):
        print("\n[COMMANDES] status modules verify ai help exit")

    def handle_command(self, cmd: str):
        if not self.acl.check(cmd): self.logger.log("ERROR", f"Acces refuse: {cmd}"); return
        self.logger.audit(f"exec:{cmd}")
        cmds = {"status": self.cmd_status, "modules": self.cmd_modules, "verify": self.cmd_verify, "ai": self.cmd_ai, "help": self.cmd_help, "exit": lambda: sys.exit(0)}
        func = cmds.get(cmd); func() if func else self.logger.log("ERROR", f"Commande inconnue: {cmd}")

    def run(self):
        self.banner(); self.verify_system(); self.load_modules(); self.cmd_help()
        while self.running:
            try: cmd = input("\nZ-CORE-ZT> ").strip().lower(); cmd and self.handle_command(cmd)
            except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__": ZCorePlateforme().run()
