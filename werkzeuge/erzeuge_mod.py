#!/usr/bin/env python3
"""Erzeugt alle Skript- und Lokalisierungsdateien der Mod aus werkzeuge/ratschlaege.py.

Aufruf (aus dem Wurzelordner der Mod):

    python3 werkzeuge/erzeuge_mod.py

Die erzeugten Dateien werden mit eingecheckt, damit die Mod ohne Python spielbar ist.
Nicht von Hand ändern: Änderungen gehören in ratschlaege.py oder in dieses Skript.
"""

import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ratschlaege import RATSCHLAEGE  # noqa: E402

WURZEL = Path(__file__).resolve().parent.parent
BOM = "﻿"
KOPF = "# Erzeugt von werkzeuge/erzeuge_mod.py – nicht von Hand ändern.\n\n"

STUFEN = ("kritisch", "warnung", "tipp")
STUFEN_TEXT = {
    "de": {"kritisch": "Akut", "warnung": "Warnung", "tipp": "Tipp"},
    "en": {"kritisch": "Critical", "warnung": "Warning", "tipp": "Tip"},
}
# Darstellung in der Warnleiste je Stufe
WARNUNG_ART = {
    "kritisch": {"type": "alert", "color": "red", "texture": "berater_kritisch"},
    "warnung": {"type": "alert", "color": "yellow", "texture": "berater_warnung"},
    "tipp": {"type": "important_action", "color": "green", "texture": "berater_tipp"},
}

# Sprachen, die Victoria 3 kennt. Deutsch hat eigene Texte, alle anderen erhalten die englischen.
SPRACHEN = [
    "english", "german", "french", "spanish", "polish", "russian",
    "japanese", "simp_chinese", "korean", "braz_por", "turkish",
]

# Feste Texte (Journal, Knöpfe, Ereignisse, Warngruppe)
TEXTE = {
    "de": {
        "je_group_berater": "Berater",
        "je_berater": "Der Berater",
        "je_berater_reason": "Dein Berater beobachtet laufend Haushalt, Bevölkerung, Politik, Markt und Diplomatie deines Landes und sagt dir, wo es hakt und was du tun kannst. Akute Probleme und Warnungen erscheinen zusätzlich live in der Warnleiste oben.",
        "je_berater_status_kopf": "Aktuelle Einschätzung:",
        "je_berater_status_alles_gut": "\\nKeine Probleme gefunden. Weiter so!",
        "berater_knopf_bericht": "Bericht anfordern",
        "berater_knopf_bericht_desc": "Der Berater erstellt sofort einen ausführlichen Bericht mit allen Befunden und Ratschlägen.",
        "berater_knopf_jahresbericht_an": "Jahresbericht: an",
        "berater_knopf_jahresbericht_aus": "Jahresbericht: aus",
        "berater_knopf_jahresbericht_desc": "Schaltet den automatischen Bericht einmal im Jahr ein oder aus.",
        "berater_knopf_krisen_an": "Krisenwarnungen: an",
        "berater_knopf_krisen_aus": "Krisenwarnungen: aus",
        "berater_knopf_krisen_desc": "Schaltet die Popup-Warnung bei akuten Problemen ein oder aus. Sie erscheint höchstens alle sechs Monate.",
        "berater.1.t": "Bericht des Beraters",
        "berater.1.d": "Exzellenz, hier ist meine Einschätzung der Lage unseres Landes.",
        "berater.1.f": "„Wer regieren will, muss vorausschauen.“",
        "berater.1.a": "Danke, ich kümmere mich darum.",
        "berater.2.t": "Der Berater schlägt Alarm",
        "berater.2.d": "Exzellenz, verzeiht die Störung, aber die Lage duldet keinen Aufschub:",
        "berater.2.f": "Akute Probleme erscheinen auch live in der Warnleiste. Diese Warnung kommt höchstens alle sechs Monate.",
        "berater.2.a": "Verstanden.",
        "berater.2.b": "Zeig mir den vollständigen Bericht.",
        "berater.2.c": "Keine Krisenwarnungen mehr.",
        "berater_bericht_kopf_kritisch": "\\n\\nAKUTE PROBLEME",
        "berater_bericht_kopf_warnung": "\\n\\nWARNUNGEN",
        "berater_bericht_kopf_tipp": "\\n\\nTIPPS",
        "berater_bericht_alles_gut": "\\n\\nIch sehe derzeit keine Probleme. Unser Land ist gut aufgestellt, Exzellenz.",
        "berater_bericht_rat": "Rat",
        "berater_warnung_aktion": "Mehr dazu im Journal unter „Der Berater“.",
        "ag_berater_tipps_name": "Tipps des Beraters",
        "ag_berater_tipps_desc": "Verbesserungsvorschläge deines Beraters",
        "ag_berater_tipps_tooltip": "Dein Berater hat Vorschläge, was du besser machen kannst.",
    },
    "en": {
        "je_group_berater": "Advisor",
        "je_berater": "The Advisor",
        "je_berater_reason": "Your advisor keeps a constant eye on your country's budget, population, politics, market and diplomacy and tells you where things go wrong and what you can do about it. Critical problems and warnings also show up live in the alert bar at the top.",
        "je_berater_status_kopf": "Current assessment:",
        "je_berater_status_alles_gut": "\\nNo problems found. Keep it up!",
        "berater_knopf_bericht": "Request Report",
        "berater_knopf_bericht_desc": "Your advisor immediately writes a detailed report with all findings and advice.",
        "berater_knopf_jahresbericht_an": "Yearly report: on",
        "berater_knopf_jahresbericht_aus": "Yearly report: off",
        "berater_knopf_jahresbericht_desc": "Turns the automatic yearly report on or off.",
        "berater_knopf_krisen_an": "Crisis warnings: on",
        "berater_knopf_krisen_aus": "Crisis warnings: off",
        "berater_knopf_krisen_desc": "Turns the popup warning for critical problems on or off. It appears at most every six months.",
        "berater.1.t": "The Advisor's Report",
        "berater.1.d": "Your Excellency, here is my assessment of our country's situation.",
        "berater.1.f": "“To govern is to foresee.”",
        "berater.1.a": "Thank you, I will see to it.",
        "berater.2.t": "The Advisor Sounds the Alarm",
        "berater.2.d": "Your Excellency, forgive the interruption, but this cannot wait:",
        "berater.2.f": "Critical problems are also shown live in the alert bar. This warning appears at most every six months.",
        "berater.2.a": "Understood.",
        "berater.2.b": "Show me the full report.",
        "berater.2.c": "No more crisis warnings.",
        "berater_bericht_kopf_kritisch": "\\n\\nCRITICAL PROBLEMS",
        "berater_bericht_kopf_warnung": "\\n\\nWARNINGS",
        "berater_bericht_kopf_tipp": "\\n\\nTIPS",
        "berater_bericht_alles_gut": "\\n\\nI see no problems at the moment. Our country is in good shape, Your Excellency.",
        "berater_bericht_rat": "Advice",
        "berater_warnung_aktion": "More in the journal under “The Advisor”.",
        "ag_berater_tipps_name": "Advisor's Tips",
        "ag_berater_tipps_desc": "Suggestions from your advisor",
        "ag_berater_tipps_tooltip": "Your advisor has suggestions on what you could do better.",
    },
}


# ---------------------------------------------------------------- Hilfsfunktionen

def bedingung(eintrag, tiefe):
    """Die Bedingung eines Ratschlags, eingerückt mit `tiefe` Tabs."""
    zeilen = textwrap.dedent(eintrag["bedingung"]).strip().splitlines()
    zeilen = [re.sub(r"^( {4})+", lambda m: "\t" * (len(m.group(0)) // 4), z) for z in zeilen]
    return "\n".join("\t" * tiefe + z for z in zeilen)


def nach_stufe(stufe):
    return [e for e in RATSCHLAEGE if e["stufe"] == stufe]


def schreibe(pfad, inhalt):
    ziel = WURZEL / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(BOM + inhalt, encoding="utf-8", newline="\n")
    print(f"  {pfad}")


def pruefe_klammern(pfad, inhalt):
    tiefe = 0
    for nr, zeile in enumerate(inhalt.splitlines(), 1):
        code = zeile.split("#", 1)[0]
        tiefe += code.count("{") - code.count("}")
        if tiefe < 0:
            sys.exit(f"{pfad}:{nr}: schließende Klammer ohne öffnende")
    if tiefe != 0:
        sys.exit(f"{pfad}: {tiefe} Klammer(n) nicht geschlossen")


def skript(pfad, inhalt):
    pruefe_klammern(pfad, inhalt)
    schreibe(pfad, KOPF + inhalt)


def pruefe_tabelle():
    gesehen = set()
    for e in RATSCHLAEGE:
        k = e["schluessel"]
        if not re.fullmatch(r"[a-z_]+", k):
            sys.exit(f"Ungültiger Schlüssel: {k!r}")
        if k in gesehen:
            sys.exit(f"Schlüssel doppelt: {k}")
        if e["stufe"] not in STUFEN:
            sys.exit(f"{k}: unbekannte Stufe {e['stufe']!r}")
        for sprache in ("de", "en"):
            if len(e[sprache]) != 3 or not all(e[sprache]):
                sys.exit(f"{k}: Texte ({sprache}) unvollständig")
        gesehen.add(k)


# ---------------------------------------------------------------- Skripte

def scripted_triggers():
    teile = ["# Jede Prüfung des Beraters als eigener Trigger im Länder-Scope: berater_problem_<schluessel> = yes\n"]
    for e in RATSCHLAEGE:
        teile.append(f"berater_problem_{e['schluessel']} = {{\n{bedingung(e, 1)}\n}}\n")

    def sammel(name, eintraege, kommentar):
        oder = "\n".join(f"\t\tberater_problem_{e['schluessel']} = yes" for e in eintraege)
        return f"# {kommentar}\n{name} = {{\n\tOR = {{\n{oder}\n\t}}\n}}\n"

    teile.append(sammel("berater_hat_problem", RATSCHLAEGE, "Irgendein Befund liegt vor"))
    for stufe in STUFEN:
        teile.append(sammel(f"berater_hat_problem_{stufe}", nach_stufe(stufe), f"Mindestens ein Befund der Stufe „{stufe}“"))
    return "\n".join(teile)


def script_values():
    return """# Wöchentliche Einnahmen minus Ausgaben des Staates
berater_wochenbilanz = {
\tvalue = income
\tsubtract = expenses
}

# Anteil der Bevölkerung, der unter dem erwarteten Lebensstandard lebt (0 bis 1)
berater_anteil_unter_erwartung = {
\tvalue = 0
\tif = {
\t\tlimit = { total_population > 0 }
\t\tvalue = population_below_expected_sol
\t\tdivide = total_population
\t}
}
"""


def alert_types():
    teile = ["# Live-Warnungen in der Warnleiste. Jede lässt sich in den Warnungseinstellungen des Spiels einzeln abschalten.\n"]
    for e in RATSCHLAEGE:
        if not e["warnung"]:
            continue
        art = WARNUNG_ART[e["stufe"]]
        gruppe = "\talert_group = berater_tipps\n" if e["stufe"] == "tipp" else ""
        teile.append(
            f"berater_{e['schluessel']} = {{\n"
            f"\tscript_context = player_country\n"
            f"\ttexture = \"gfx/interface/icons/berater/{art['texture']}.dds\"\n"
            f"\ttype = {art['type']}\n"
            f"{gruppe}"
            f"\tcolor = {art['color']}\n"
            f"\tvalid = {{\n"
            f"\t\tberater_problem_{e['schluessel']} = yes\n"
            f"\t}}\n"
            f"}}\n"
        )
    return "\n".join(teile)


def alert_groups():
    return "# Fasst die Tipps des Beraters in der Warnleiste zu einem Eintrag zusammen\nberater_tipps = {\n}\n"


def journal_entry_groups():
    return "je_group_berater = {\n\tcontext = country\n}\n"


def journal_entries():
    status = []
    for stufe in STUFEN:
        for e in nach_stufe(stufe):
            status.append(
                f"\t\ttriggered_desc = {{\n"
                f"\t\t\tdesc = je_berater_status_{e['schluessel']}\n"
                f"\t\t\ttrigger = {{ berater_problem_{e['schluessel']} = yes }}\n"
                f"\t\t}}"
            )
    status = "\n".join(status)
    return f"""# Das Journal des Beraters: wird für jeden Spieler automatisch aktiv und zeigt live alle Befunde.
je_berater = {{
\tgroup = je_group_berater
\ticon = "gfx/interface/icons/event_icons/event_scales.dds"

\tis_shown_when_inactive = {{
\t\tis_player = yes
\t}}
\tpossible = {{
\t\tis_player = yes
\t}}
\tinvalid = {{
\t\tis_player = no
\t}}

\ttransferable = yes
\tweight = 1
\tshould_update_on_player_command = yes

\tstatus_desc = {{
\t\tdesc = je_berater_status_kopf
{status}
\t\ttriggered_desc = {{
\t\t\tdesc = je_berater_status_alles_gut
\t\t\ttrigger = {{ berater_hat_problem = no }}
\t\t}}
\t}}

\tscripted_button = berater_knopf_bericht
\tscripted_button = berater_knopf_jahresbericht
\tscripted_button = berater_knopf_krisen
}}
"""


def umschalter(name, variable):
    """Knopf, der eine Ländervariable umschaltet. Ohne Variable ist die Funktion an."""
    return f"""{name} = {{
\tname = {{
\t\tfirst_valid = {{
\t\t\ttriggered_desc = {{
\t\t\t\tdesc = {name}_aus
\t\t\t\ttrigger = {{ has_variable = {variable} }}
\t\t\t}}
\t\t\tdesc = {name}_an
\t\t}}
\t}}
\tdesc = {name}_desc
\tvisible = {{ always = yes }}
\tpossible = {{ always = yes }}
\teffect = {{
\t\tif = {{
\t\t\tlimit = {{ has_variable = {variable} }}
\t\t\tremove_variable = {variable}
\t\t}}
\t\telse = {{
\t\t\tset_variable = {variable}
\t\t}}
\t}}
\tai_chance = {{
\t\tvalue = 0
\t}}
}}
"""


def scripted_buttons():
    bericht = """berater_knopf_bericht = {
\tname = berater_knopf_bericht
\tdesc = berater_knopf_bericht_desc
\tvisible = { always = yes }
\tpossible = { always = yes }
\teffect = {
\t\ttrigger_event = { id = berater.1 popup = yes }
\t}
\tai_chance = {
\t\tvalue = 0
\t}
}
"""
    return "\n".join([
        "# Knöpfe im Journal des Beraters\n",
        bericht,
        umschalter("berater_knopf_jahresbericht", "berater_kein_jahresbericht"),
        umschalter("berater_knopf_krisen", "berater_keine_krisenwarnungen"),
    ])


def on_actions():
    return """# Hängt die Prüfungen an die monatlichen und jährlichen Takte des Spiels an.
# Die Listen werden mit den Listen des Grundspiels und anderer Mods zusammengeführt.
on_monthly_pulse_country = {
\ton_actions = { berater_monatlich }
}

on_yearly_pulse_country = {
\ton_actions = { berater_jaehrlich }
}

# Krisenwarnung als Popup, höchstens alle sechs Monate
berater_monatlich = {
\ttrigger = {
\t\tis_player = yes
\t\tNOT = { has_variable = berater_keine_krisenwarnungen }
\t\tNOT = { has_variable = berater_krisenwarnung_pause }
\t\tberater_hat_problem_kritisch = yes
\t}
\teffect = {
\t\tset_variable = {
\t\t\tname = berater_krisenwarnung_pause
\t\t\tmonths = 6
\t\t}
\t\ttrigger_event = { id = berater.2 popup = yes }
\t}
}

# Jahresbericht
berater_jaehrlich = {
\ttrigger = {
\t\tis_player = yes
\t\tNOT = { has_variable = berater_kein_jahresbericht }
\t}
\tevents = { berater.1 }
}
"""


def bericht_desc(eintraege_je_stufe, einrueckung):
    """complex_desc mit Abschnitt je Stufe; jeder Befund nur, wenn er vorliegt."""
    t = "\t" * einrueckung
    teile = []
    for stufe, eintraege in eintraege_je_stufe:
        if not eintraege:
            continue
        teile.append(
            f"{t}triggered_desc = {{\n"
            f"{t}\tdesc = berater_bericht_kopf_{stufe}\n"
            f"{t}\ttrigger = {{ berater_hat_problem_{stufe} = yes }}\n"
            f"{t}}}"
        )
        for e in eintraege:
            teile.append(
                f"{t}triggered_desc = {{\n"
                f"{t}\tdesc = berater_bericht_{e['schluessel']}\n"
                f"{t}\ttrigger = {{ berater_problem_{e['schluessel']} = yes }}\n"
                f"{t}}}"
            )
    return "\n".join(teile)


def events():
    alle = bericht_desc([(s, nach_stufe(s)) for s in STUFEN], 2)
    kritisch = bericht_desc([("kritisch", nach_stufe("kritisch"))], 2)
    return f"""namespace = berater

# Vollständiger Bericht: über den Journal-Knopf oder einmal im Jahr
berater.1 = {{
\ttype = country_event
\ttitle = berater.1.t
\tdesc = {{
\t\tdesc = berater.1.d
{alle}
\t\ttriggered_desc = {{
\t\t\tdesc = berater_bericht_alles_gut
\t\t\ttrigger = {{ berater_hat_problem = no }}
\t\t}}
\t}}
\tflavor = berater.1.f
\tevent_image = {{
\t\ttexture = "gfx/event_pictures/unspecific_politicians_arguing.dds"
\t}}
\ticon = "gfx/interface/icons/event_icons/event_scales.dds"
\tduration = 3

\ttrigger = {{
\t\tis_player = yes
\t}}

\toption = {{
\t\tname = berater.1.a
\t\tdefault_option = yes
\t}}
}}

# Krisenwarnung: nur akute Probleme, ausgelöst von berater_monatlich
berater.2 = {{
\ttype = country_event
\ttitle = berater.2.t
\tdesc = {{
\t\tdesc = berater.2.d
{kritisch}
\t}}
\tflavor = berater.2.f
\tevent_image = {{
\t\ttexture = "gfx/event_pictures/unspecific_politicians_arguing.dds"
\t}}
\ticon = "gfx/interface/icons/event_icons/event_scales.dds"
\tduration = 3

\ttrigger = {{
\t\tis_player = yes
\t\tberater_hat_problem_kritisch = yes
\t}}

\toption = {{
\t\tname = berater.2.a
\t\tdefault_option = yes
\t}}
\toption = {{
\t\tname = berater.2.b
\t\ttrigger_event = {{ id = berater.1 popup = yes }}
\t}}
\toption = {{
\t\tname = berater.2.c
\t\tset_variable = berater_keine_krisenwarnungen
\t}}
}}
"""


# ---------------------------------------------------------------- Lokalisierung

def loc_text(text):
    # Gerade Anführungszeichen beenden in Paradox-Lokalisierung den Text; typografische verwenden
    if '"' in text:
        sys.exit(f"Gerades Anführungszeichen im Text: {text!r}")
    return text


def lokalisierung(sprache_kurz):
    texte = dict(TEXTE[sprache_kurz])
    stufen = STUFEN_TEXT[sprache_kurz]
    rat = texte["berater_bericht_rat"]
    for e in RATSCHLAEGE:
        k = e["schluessel"]
        titel, befund, ratschlag = e[sprache_kurz]
        stufe = stufen[e["stufe"]]
        texte[f"je_berater_status_{k}"] = f"\\n• {stufe}: {titel}"
        texte[f"berater_bericht_{k}"] = f"\\n\\n• {titel}\\n{befund}\\n{rat}: {ratschlag}"
        if e["warnung"]:
            texte[f"alert_berater_{k}_name"] = f"{titel}"
            texte[f"alert_berater_{k}_desc"] = befund
            texte[f"alert_berater_{k}_hint"] = f"{rat}: {ratschlag}"
            texte[f"alert_berater_{k}_action"] = texte["berater_warnung_aktion"]
            texte[f"berater_{k}_setting_name"] = f"{texte['je_berater']}: {titel}"
    return texte


def schreibe_lokalisierung():
    for sprache in SPRACHEN:
        texte = lokalisierung("de" if sprache == "german" else "en")
        zeilen = [f"l_{sprache}:"]
        zeilen += [f' {k}: "{loc_text(v)}"' for k, v in texte.items()]
        schreibe(f"localization/{sprache}/berater_l_{sprache}.yml", "\n".join(zeilen) + "\n")


# ---------------------------------------------------------------- Hauptprogramm

def main():
    pruefe_tabelle()
    print(f"{len(RATSCHLAEGE)} Ratschläge, schreibe:")
    skript("common/scripted_triggers/berater_scripted_triggers.txt", scripted_triggers())
    skript("common/script_values/berater_script_values.txt", script_values())
    skript("common/alert_types/berater_alert_types.txt", alert_types())
    skript("common/alert_groups/berater_alert_groups.txt", alert_groups())
    skript("common/journal_entry_groups/berater_journal_entry_groups.txt", journal_entry_groups())
    skript("common/journal_entries/berater_journal_entries.txt", journal_entries())
    skript("common/scripted_buttons/berater_scripted_buttons.txt", scripted_buttons())
    skript("common/on_actions/berater_on_actions.txt", on_actions())
    skript("events/berater_events.txt", events())
    schreibe_lokalisierung()


if __name__ == "__main__":
    main()
