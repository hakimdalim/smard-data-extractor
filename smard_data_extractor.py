import time
from datetime import datetime
import requests
import pandas as pd
from io import BytesIO
from functools import reduce

# Zeitbereich 
dt_from = datetime(2024, 7, 1, 0, 0)
dt_to = datetime(2025, 7, 1)
timestamp_from = int(time.mktime(dt_from.timetuple()) * 1000)
timestamp_to = int(time.mktime(dt_to.timetuple()) * 1000)

# API-Endpunkt
url = 'https://www.smard.de/nip-download-manager/nip/download/market-data'

# Modul-ID → Klarname für Spaltennamen
module_map = {
    1004067: "Wind Onshore [MW]",
    1004068: "Photovoltaik [MW]",
    1004071: "Erdgas [MW]",
    5000410: "Verbrauch [MW]",
    8004169: "Deutschland/Luxemburg [€/MWh]"
}

# Payload erzeugen
def create_payload(module_id):
    return {
        "request_form": [{
            "format": "CSV",
            "moduleIds": [module_id],
            "region": "DE",
            "timestamp_from": timestamp_from,
            "timestamp_to": timestamp_to,
            "type": "discrete",
            "language": "de",
            "resolution": "hour"
        }]
    }

# CSV laden und Datum + Werte parsen
def fetch_module_data(module_id, target_name):
    print(f"⏳ Lade: {target_name}")
    response = requests.post(url, json=create_payload(module_id))
    if response.ok:
        # CSV als Text analysieren
        content = response.content.decode("utf-8")
        lines = content.strip().split("\n")

        # Auflösungszeile suchen (meistens letzte Zeile)
        aufloesung = None
        for line in reversed(lines):
            if "Originalauflösungen" in line or "Viertelstunde" in line or "Stündlich" in line:
                aufloesung = line.strip()
                break

        # Jetzt CSV erneut korrekt einlesen (ohne Fußzeile)
        df = pd.read_csv(BytesIO(response.content), sep=";", encoding="utf-8", skipfooter=1, engine="python")

        if "Datum von" not in df.columns or "Datum bis" not in df.columns:
            print(f"Ungültige Struktur in Modul {module_id}")
            return pd.DataFrame()

        # Messwert-Spalte ermitteln
        messwert_spalte = [c for c in df.columns if c not in ["Datum von", "Datum bis"]][0]
        df = df.rename(columns={messwert_spalte: messwert_spalte})

        return df[["Datum von", "Datum bis", messwert_spalte]]
    else:
        print(f" Fehler bei Modul {module_id}: {response.status_code}")
        return pd.DataFrame()

# Daten laden
dfs = []
for module_id, name in module_map.items():
    df = fetch_module_data(module_id, name)
    if not df.empty:
        dfs.append(df)

# Join über Zeitspalten
df_merged = reduce(lambda left, right: pd.merge(left, right, on=["Datum von", "Datum bis"], how="outer"), dfs)
df_merged = df_merged.sort_values("Datum von")

# Speichern
df_merged.to_csv("juli24-25_energie_zusammengefasst_mit_aufloesung.csv", sep=";", index=False)
print("datei geschrieben: juli24-25_energie_zusammengefasst_mit_aufloesung.csv")
