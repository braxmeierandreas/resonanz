# -*- coding: utf-8 -*-
"""
Auswertung Pretest RESONANZ
===========================
Liest den SoSci Survey Export ein, berechnet Kennwerte und erstellt 
die Diagramme für den Pretest-Bericht.
"""

import statistics as st
from collections import Counter
import openpyxl
import traceback
import os
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1 Einstellungen
# ----------------------------------------------------------------------

DATEI = r"Pretest_Export_soscisurvey.xlsx"

ITEMS = {
    "A103": "F4b Mentaler Gesundheitszustand",
    "A104": "F4c Stress im Studienalltag",
    "A201": "F5  App klingt interessant",
    "A202": "F6  App-Foerderung sinnvoll",
    "A203": "F7  Kombination Profil und Empfehlung",
    "A204": "F8  Punktesystem motiviert",
    "A205": "F8a Punkte sammeln motivierend",
    "A206": "F8b Gamification spricht an",
    "A207": "F9  Wuerde die App ausprobieren",
    "A208": "F10 Mehrwoechige Nutzung",
    "A301": "F11 Funktionsweise verstaendlich",
    "A302": "F12 Inhalte passen zum Ziel",
    "A303": "F13 Datenschutz-Bedenken (negativ gepolt)",
    "A304": "F13b Tracking bei klarem Nutzen erlauben",
    "A305": "F14 Empfehlung durch Institution",
}

SKALEN = {
    "S1 Attraktivitaet und Akzeptanz": ["A201", "A202", "A204", "A207"],
    "S2 Nutzungsintention":            ["A207", "A208"],
    "S3 Verstaendlichkeit":            ["A301", "A302"],
    "S4 Gamification-Akzeptanz":       ["A204", "A205", "A206"],
}

KATEGORIAL = {
    "A101": ("F1  Alter", {1: "18-24", 2: "25-34", 3: "35-44", 4: "45+"}),
    "A102": ("F2  Geschlecht", {1: "weiblich", 2: "maennlich", 3: "divers", 4: "keine Angabe"}),
    "A401": ("F15 Vorerfahrung", {1: "Ja", 2: "Nein", 3: "keine Angabe"}),
    "A404": ("F16b Zahlungsbereitschaft", {1: "kostenlos", 2: "bis 2 EUR", 3: "bis 5 EUR", 4: "bis 10 EUR", 5: "ueber 10 EUR"}),
    "A405": ("F16c Preismodell", {1: "Werbung", 2: "Freemium", 3: "Einmalkauf", 4: "Abo", 5: "keine Praeferenz"}),
}

# ----------------------------------------------------------------------
# 2 Hilfsfunktionen
# ----------------------------------------------------------------------

def lade_daten(pfad):
    if not os.path.exists(pfad):
        raise FileNotFoundError(f"Die Datei '{pfad}' wurde nicht gefunden!")
    wb = openpyxl.load_workbook(pfad, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    codes = rows[0]
    idx = {c: i for i, c in enumerate(codes) if c}
    daten = rows[2:]
    return idx, daten

def wert(zeile, code, idx):
    if code not in idx: return None
    v = zeile[idx[code]]
    return None if v in (None, "") else v

def zahlen(code, idx, daten):
    out = []
    for z in daten:
        v = wert(z, code, idx)
        if v is not None:
            try: out.append(float(v))
            except (TypeError, ValueError): pass
    return out

def kennwerte(code, idx, daten):
    v = zahlen(code, idx, daten)
    if not v: return None
    return len(v), round(st.mean(v), 2), round(st.pstdev(v), 2)

def skalenwert(items, idx, daten):
    pro_person = []
    for z in daten:
        werte = [wert(z, c, idx) for c in items]
        if all(w is not None for w in werte):
            pro_person.append(st.mean(float(w) for w in werte))
    if not pro_person: return None
    return len(pro_person), round(st.mean(pro_person), 2), round(st.pstdev(pro_person), 2)

# ----------------------------------------------------------------------
# 3 Hauptfunktionen
# ----------------------------------------------------------------------

def main():
    idx, daten = lade_daten(DATEI)
    print("\n--- AUSWERTUNG STARTET ---")
    fertig = sum(1 for z in daten if str(wert(z, "FINISHED", idx)) == "1")
    print(f"Aufrufe insgesamt: {len(daten)}")
    print(f"Vollstaendige Bearbeitungen: {fertig}")

def grafiken():
    print(f"Speichere Grafiken in: {os.getcwd()}")
    idx, daten = lade_daten(DATEI)
    HFU, MEDIUM, HELL, GRAU = "#00893A", "#5FB878", "#BEE3C8", "#888888"

    # --- Abbildung 1: Skalen (Design-Version) ---
    name_map = {
        "S1": "S1\nAttraktivität",
        "S2": "S2\nNutzungsintention",
        "S3": "S3\nVerständlichkeit",
        "S4": "S4\nGamification"
    }

    namen, mittel, streu = [], [], []
    for name, items in SKALEN.items():
        k = skalenwert(items, idx, daten)
        if k:
            kurzname = name.split()[0]
            namen.append(name_map.get(kurzname, kurzname))
            mittel.append(k[1])
            streu.append(k[2])
    
    if namen:
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(namen, mittel, yerr=streu, capsize=6, color=HFU, edgecolor="black", width=0.6)
        
        ax.set_ylim(1, 5)
        ax.set_ylabel("Mittelwert (1–5)", fontsize=12)
        ax.axhline(3, color=GRAU, linestyle="--", linewidth=1.5)
        ax.text(0.5, 3.05, "Skalenmitte (3)", color=GRAU, fontsize=9)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar, m in zip(bars, mittel):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{m:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig("abb1_skalen.png", dpi=300)
        plt.close()
        print("-> abb1_skalen.png gespeichert.")

    # --- Abbildung 2: Einzelitems ---
    codes = ["A201", "A202", "A203", "A204", "A205", "A206", "A207", "A208"]
    labels = ["F5", "F6", "F7", "F8", "F8a", "F8b", "F9", "F10"]
    # Passende Klartext-Labels für die Legende (optional, hier direkt im Plot)
    werte = [kennwerte(c, idx, daten)[1] for c in codes if kennwerte(c, idx, daten)]
    
    if werte:
        fig, ax = plt.subplots(figsize=(7, 4))
        farben = [HFU if v >= 4.0 else HELL if v < 3.5 else MEDIUM for v in werte]
        
        bars = ax.barh(range(len(werte))[::-1], werte, color=farben, edgecolor="black", height=0.7)
        ax.set_yticks(range(len(werte))[::-1])
        ax.set_yticklabels(labels, fontsize=12)
        ax.set_xlim(1, 5)
        ax.set_xlabel("Mittelwert (1–5)", fontsize=12)
        ax.axvline(3, color=GRAU, linestyle="--")
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, 
                    f'{width:.2f}', va='center', fontweight='bold', fontsize=11)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig("abb2_items.png", dpi=300)
        plt.close()
        print("-> abb2_items.png gespeichert.")

# ----------------------------------------------------------------------
# Startpunkt
# ----------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
        grafiken()
        print("\n--- Erfolgreich abgeschlossen ---")
    except Exception:
        print("\n" + "!" * 50)
        print("FEHLER AUFGETRETEN:")
        traceback.print_exc()
        print("!" * 50)
    
    input("\nDrücke die Enter-Taste, um das Fenster zu schließen...")