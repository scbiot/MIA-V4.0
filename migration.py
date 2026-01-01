import re
import json
import os

BASE_DIR = r"h:\Mi unidad\4-WATER TECH S.A\GEMINI- ideas y accciones estrategicas\Inteligencia Comercial\MIA\MIA V4.0"
INFO_DIR = os.path.join(BASE_DIR, "Información previa")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

def migrate_portals():
    file_path = os.path.join(INFO_DIR, "Inventario de plataformas de compras.txt")
    if not os.path.exists(file_path):
        print("Inventory file not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract domains using regex: site:([domain])
    domains = re.findall(r'site:([\w\.-]+)', content)
    
    portals = []
    seen = set()
    for d in domains:
        if d in seen: continue
        seen.add(d)
        
        portals.append({
            "name": d,
            "url": f"https://{d}", # Assumption
            "type": "Detected",
            "search_method": "Google Dork", # Marking as dork-derived
            "enabled": True,
            "notes": "Imported from Google Alerts Inventory"
        })
    
    with open(os.path.join(CONFIG_DIR, "portals.json"), 'w', encoding='utf-8') as f:
        json.dump(portals, f, indent=2, ensure_ascii=False)
    print(f"Migrated {len(portals)} portals.")

def migrate_keywords():
    rubro_files = {
        "Rubro 1: Purificación - Ingeniería": "Palabras Clave - Rubro I.txt",
        "Rubro 2: Purificación - Provisión": "Palabras Clave - Rubro II.txt",
        "Rubro 3: Purificación - Servicios": "Palabras Clave - Rubro III.txt",
        "Rubro 4: Purificación - Gestión Hídrica": "Palabras Clave - Rubro IV.txt",
        "Rubro 5: Efluentes - Ingeniería": "Palabras Clave - Rubro V.txt",
        "Rubro 6: Efluentes - Provisión": "Palabras Clave - Rubro VI.txt",
        "Rubro 7: Efluentes - Servicios": "Palabras Clave - Rubro VII.txt",
        "Rubro 8: Efluentes - Gestión Hídrica": "Palabras Clave - Rubro VIII.txt",
    }
    
    keywords_config = {
        "triggers": [],
        "rubros": {},
        "vital_water_keywords": {
            "description": "Keywords for Vital Water (Rubro 2 & 3)",
            "rubro_2_products": ["Ablandador", "Osmosis Inversa", "Filtro"], # Placeholder/Merged later if needed
            "rubro_3_products": ["Cartucho", "Sal", "Resina"]
        }
    }

    # Load Triggers
    trigger_path = os.path.join(INFO_DIR, "Palabras Clave - Disparadores de Oportunidad.txt")
    if os.path.exists(trigger_path):
        with open(trigger_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Extract phrases inside quotes "..."
            triggers = []
            for line in lines:
                m = re.search(r'"([^"]+)"', line)
                if m:
                    triggers.append(m.group(1))
            keywords_config['triggers'] = triggers

    # Load Rubros
    for rubro_name, filename in rubro_files.items():
        path = os.path.join(INFO_DIR, filename)
        keywords = []
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Match lines like "1. Keyword..." or just "Keyword"
                    # Remove numbering "1. ", "32. "
                    clean = re.sub(r'^\d+\.\s*', '', line)
                    if clean and not clean.startswith("I.") and not clean.startswith("Rubro") and len(clean) > 2:
                         keywords.append(clean)
        keywords_config['rubros'][rubro_name] = keywords

    with open(os.path.join(CONFIG_DIR, "keywords.json"), 'w', encoding='utf-8') as f:
        json.dump(keywords_config, f, indent=2, ensure_ascii=False)
    print("Migrated Keywords.")

if __name__ == "__main__":
    migrate_portals()
    migrate_keywords()
