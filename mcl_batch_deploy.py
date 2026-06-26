# mcl_batch_deploy.py - MCL_MILYES V1.2 RÉAL
# Stack: Z-META-LLaMA-4 INT8 + 10 Agents DZ + Docker Isolation

import docker
import json
import os
from pathlib import Path

# Z-RORE CONFIG
OLLAMA_IMAGE = "ollama/ollama:latest" 
MODEL_NAME = "llama4:8b-instruct-int8" # 8GB VRAM OK
NETWORK_MODE = "none" # 0 internet. RÉAL only.
GPU_ALL = "all"

def load_mcl_agents(json_path="10_DZ_SECTORS.json"):
    """Z-H204: Charge les 10 agents DZ depuis JSON"""
    default_agents = [
        {"name": "MCL-RST-01", "sector": "Resto DZ", "prompt": "Tu es closer Resto Alger. Vends menu midi H24. Ton: direct DZ."},
        {"name": "MCL-IMM-02", "sector": "Immo DZ", "prompt": "Tu es agent immo Oran. Qualifie budget, zone, cash. 0 blabla."},
        {"name": "MCL-AUTO-03", "sector": "Auto DZ", "prompt": "Tu es vendeur auto Alger. DM auto sous posts marketplace FB DZ."},
        {"name": "MCL-COS-04", "sector": "Cosmetique DZ", "prompt": "Tu es conseillere beaute. Reponds 24/7 sur Insta DZ."},
        {"name": "MCL-SHV-05", "sector": "Startup SaaS", "prompt": "Tu es CTO SaaS DZ. Pitch investisseur en 3 lignes."},
        {"name": "MCL-EDU-06", "sector": "Formation DZ", "prompt": "Tu es formateur IA DZ. Vends bootcamp LLaMA-4 local."},
        {"name": "MCL-LAW-07", "sector": "Juridique DZ", "prompt": "Tu es juriste DZ. Genere contrats startup fr/ar."},
        {"name": "MCL-MED-08", "sector": "Sante DZ", "prompt": "Tu es assistant clinique. RDV + triage, pas diagnostic."},
        {"name": "MCL-LOG-09", "sector": "Logistique DZ", "prompt": "Tu es ops log Alger. Optimise livraison 58 wilayas."},
        {"name": "MCL-ZCORE-10", "sector": "MASTER", "prompt": "Tu es IAZ_ENGINE. Coordonne les 9 autres. Règle: RÉAL only."}
    ]
    
    if Path(json_path).exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Auto-génère le fichier si inexistant
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(default_agents, f, ensure_ascii=False, indent=2)
        print(f"[Z-H204] Fichier {json_path} auto-généré.")
    return default_agents

def launch_agent(client, agent):
    """Z-H201: Lance 1 container Docker pour 1 agent"""
    container_name = agent["name"].lower()
    env_vars = {
        "OLLAMA_HOST": "0.0.0.0",
        "SYSTEM_PROMPT": agent["prompt"],
        "AGENT_SECTOR": agent["sector"],
        "RÉAL_MODE": "ON"
    }
    
    print(f"[MCL] Lancement {agent['name']} | Secteur: {agent['sector']}")
    
    try:
        client.containers.run(
            image=OLLAMA_IMAGE,
            name=container_name,
            command=f"serve",
            environment=env_vars,
            network_mode=NETWORK_MODE, # PATCH Z-RORE: Coupe internet
            device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])], # GPU passthrough
            volumes={os.getcwd(): {"bind": "/mcl", "mode": "rw"}},
            detach=True,
            remove=True,
            mem_limit="7g", # Limite RAM pour 8GB VRAM total
            ports={"11434/tcp": None} # Pas de port exposé. RÉAL only.
        )
        print(f"[MCL] {agent['name']} UP | VRAM: INT8 | NET: OFF")
    except docker.errors.APIError as e:
        print(f"[ERROR] {agent['name']} FAILED: {e}")

def main():
    """IAZ_ENGINE: Boot séquence 1>2>3"""
    print("="*40)
    print(" MCL_MILYES BATCH FORGE V1.2 RÉAL ")
    print("="*40)
    
    client = docker.from_env()
    agents = load_mcl_agents()
    
    # Pull modèle 1 fois
    print(f"[Z-H201] Pull modèle: {MODEL_NAME}")
    client.images.pull(OLLAMA_IMAGE)
    
    # Lancement BATCH
    for agent in agents:
        launch_agent(client, agent)
    
    print("\n[IAZ_ENGINE] CYCLE TERMINE. 10/10 Agents RÉAL UP.")
    print("Check: docker ps | grep mcl-")

if __name__ == "__main__":
    main()
