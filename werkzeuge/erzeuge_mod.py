#!/usr/bin/env python3
"""Erzeugt alle Skript- und Lokalisierungsdateien der Mod aus werkzeuge/ratschlaege.py und
werkzeuge/plaene.py.

Aufruf (aus dem Wurzelordner der Mod):

    python3 werkzeuge/erzeuge_mod.py

Die erzeugten Dateien werden mit eingecheckt, damit die Mod ohne Python spielbar ist.
Nicht von Hand ändern: Änderungen gehören in ratschlaege.py, plaene.py oder in dieses Skript.
"""

import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plaene import GESETZE, GUETER, MAX_GESETZE, MAX_GUETER, PREIS_SCHWELLE  # noqa: E402
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

# Sprachen, die Victoria 3 kennt. Deutsch hat eigene Texte, alle anderen erhalten die englischen
# (das Spiel greift bei fehlenden Texten nicht auf Englisch zurück).
SPRACHEN = [
    "english", "german", "french", "spanish", "polish", "russian",
    "japanese", "simp_chinese", "korean", "braz_por", "turkish",
]

# Bilder (Videos des Grundspiels, Medien-Aliasse) und Symbole der Ereignisse
EREIGNIS_BILD = {
    1: ("unspecific_politicians_arguing", "event_scales"),
    2: ("europenorthamerica_political_extremism", "event_protest"),
    3: ("middleeast_engineer_blueprint", "event_industry"),
    4: ("asia_politician_parliament_motion", "event_scales"),
}

ANZAHL_REGIERUNGSGESETZE = 3

# Feste Texte (Journal, Knöpfe, Ereignisse, Warngruppe)
TEXTE = {
    "de": {
        "je_group_berater": "Berater",
        "je_berater": "Der Berater",
        "je_berater_reason": "Dein Berater beobachtet laufend Haushalt, Bevölkerung, Politik, Markt und Diplomatie deines Landes und sagt dir, wo es hakt und was du tun kannst. Akute Probleme und Warnungen erscheinen zusätzlich live in der Warnleiste oben.\\n\\nKonkrete Anweisungen gibt es auf Knopfdruck: Der #bold Bauplan#! sagt dir, was du in welchem Staat bauen sollst, der #bold Gesetzesplan#!, welche Gesetze du als Nächstes verabschieden solltest.",
        "je_berater_status_kopf": "Aktuelle Einschätzung:",
        "je_berater_status_alles_gut": "\\nKeine Probleme gefunden. Weiter so!",
        "berater_knopf_bericht": "Lagebericht",
        "berater_knopf_bericht_desc": "Der Berater fasst alle Befunde mit Ratschlägen zusammen und nennt die betroffenen Staaten und Interessengruppen.",
        "berater_knopf_bauplan": "Bauplan",
        "berater_knopf_bauplan_desc": "Der Berater sagt dir, welche Gebäude du in welchem Staat bauen solltest.",
        "berater_knopf_gesetzesplan": "Gesetzesplan",
        "berater_knopf_gesetzesplan_desc": "Der Berater empfiehlt dir die nächsten Gesetze und sagt, ob deine Regierung sie mitträgt.",
        "berater_knopf_jahresbericht_an": "Jahresbericht: an",
        "berater_knopf_jahresbericht_aus": "Jahresbericht: aus",
        "berater_knopf_jahresbericht_desc": "Schaltet den automatischen Lagebericht einmal im Jahr ein oder aus.",
        "berater_knopf_krisen_an": "Krisenwarnungen: an",
        "berater_knopf_krisen_aus": "Krisenwarnungen: aus",
        "berater_knopf_krisen_desc": "Schaltet die Popup-Warnung bei akuten Problemen ein oder aus. Sie erscheint höchstens alle sechs Monate.",
        "berater.1.t": "Lagebericht des Beraters",
        "berater.1.d": "Exzellenz, hier ist meine Einschätzung der Lage unseres Landes.",
        "berater.1.f": "„Wer regieren will, muss vorausschauen.“",
        "berater.1.a": "Danke, ich kümmere mich darum.",
        "berater.2.t": "Der Berater schlägt Alarm",
        "berater.2.d": "Exzellenz, verzeiht die Störung, aber die Lage duldet keinen Aufschub:",
        "berater.2.f": "Akute Probleme erscheinen auch live in der Warnleiste. Diese Warnung kommt höchstens alle sechs Monate.",
        "berater.2.a": "Verstanden.",
        "berater.2.b": "Zeig mir den vollständigen Lagebericht.",
        "berater.2.c": "Keine Krisenwarnungen mehr.",
        "berater.3.t": "Bauplan des Beraters",
        "berater.3.d": "Exzellenz, diese Bauvorhaben würden unserem Land jetzt am meisten nützen. Ich habe jeweils den Staat gewählt, in dem das Gebäude möglich ist und die meisten Arbeitskräfte frei sind.",
        "berater.3.f": "Preise und Staaten beziehen sich auf den Zeitpunkt des Plans. Fordere im Journal jederzeit einen neuen an.",
        "berater.3.a": "Ich gebe die Aufträge in Bau.",
        "berater.4.t": "Gesetzesplan des Beraters",
        "berater.4.d": "Exzellenz, diese Reformen würde ich als Nächstes angehen.",
        "berater.4.f": "Ein Gesetz kommt leichter durch, wenn mächtige Interessengruppen in der Regierung es befürworten.",
        "berater.4.a": "Ich bringe das auf den Weg.",
        "berater_zeige_lagebericht": "Zeig mir den Lagebericht.",
        "berater_zeige_bauplan": "Zeig mir den Bauplan.",
        "berater_zeige_gesetzesplan": "Zeig mir den Gesetzesplan.",
        "berater_bericht_kopf_kritisch": "\\n\\n#bold AKUTE PROBLEME#!",
        "berater_bericht_kopf_warnung": "\\n\\n#bold WARNUNGEN#!",
        "berater_bericht_kopf_tipp": "\\n\\n#bold TIPPS#!",
        "berater_bericht_alles_gut": "\\n\\nIch sehe derzeit keine Probleme. Unser Land ist gut aufgestellt, Exzellenz.",
        "berater_bericht_rat": "Rat",
        "berater_bericht_hinweis_plaene": "\\n\\nWas genau du wo bauen und welche Gesetze du verabschieden solltest, steht im #bold Bauplan#! und im #bold Gesetzesplan#!.",
        "berater_warnung_aktion": "Mehr dazu im Journal unter „Der Berater“.",
        "berater_bauplan_kopf_gueter": "\\n\\n#bold TEURE GÜTER – SELBST HERSTELLEN#!",
        "berater_bauplan_kopf_infrastruktur": "\\n\\n#bold INFRASTRUKTUR#!",
        "berater_bauplan_kopf_staat": "\\n\\n#bold VERWALTUNG UND BAUWIRTSCHAFT#!",
        "berater_bauplan_infra": "\\n• #bold {STAAT}#! braucht mehr Infrastruktur, als vorhanden ist. Das bremst dort alle Betriebe. Empfehlung: #bold {BAHN}#!, an der Küste auch #bold {HAFEN}#!.",
        "berater_bauplan_verwaltung": "\\n• Deine Bürokratie reicht nicht. Empfehlung: #bold {VERWALTUNG}#! in #bold {STAAT}#!.",
        "berater_bauplan_bausektor": "\\n• Deine Bauwarteschlange ist lang und der Haushalt im Plus, also lohnt sich mehr Baukapazität. Empfehlung: #bold {BAUSEKTOR}#! in #bold {STAAT}#!.",
        "berater_bauplan_gut": "\\n• #bold {GUT}#! kostet {PREIS} mehr als der Grundpreis. Empfehlung: #bold {GEBAEUDE}#! in #bold {STAAT}#!.",
        "berater_bauplan_gut_kein_ort": "\\n• #bold {GUT}#! kostet {PREIS} mehr als der Grundpreis, aber in keinem deiner Staaten ist #bold {GEBAEUDE}#! möglich. Sichere dir Importe über Handelsrouten.",
        "berater_bauplan_nichts": "\\n\\nIm Moment drängt kein Bauvorhaben. Die Preise sind im Rahmen und die Infrastruktur reicht. Investiere in Bausektoren, Universitäten oder die Industrie, die dein Land am besten kann.",
        "berater_gesetzplan_aktuell": "\\n\\n#bold IN ARBEIT#!\\n• Du verabschiedest gerade #bold {GESETZ}#!. Bring es durch, bevor du ein neues Gesetz beginnst.",
        "berater_gesetzplan_kopf_empfehlung": "\\n\\n#bold EMPFEHLUNGEN#!",
        "berater_gesetzplan_kopf_regierung": "\\n\\n#bold DAS TRÄGT DEINE REGIERUNG MIT#!\\nDiese Gesetze kannst du jetzt einbringen, ohne dass eine Regierungspartei dagegen ist:",
        "berater_gesetzplan_unterstuetzt": " #G Deine Regierung trägt das mit.#!",
        "berater_gesetzplan_umstritten": " #Y Dafür fehlt in deiner Regierung noch Rückhalt: Nimm Interessengruppen auf, die das Gesetz befürworten.#!",
        "berater_gesetzplan_empfehlung": "\\n• Verabschiede #bold {GESETZ}#!. {GRUND}",
        "berater_gesetzplan_regierung": "\\n• #bold {GESETZ}#!",
        "berater_gesetzplan_nichts": "\\n\\nIm Moment habe ich keine Gesetzesempfehlung. Deine Gesetze passen zur Lage, oder die nächsten Reformen sind noch nicht erforscht.",
        "berater_gesetzplan_warten": "\\n\\nSobald das aktuelle Gesetz durch ist, kann ich dir weitere empfehlen.",
        "berater_detail_einleitung": "\\n",
        "ag_berater_tipps_name": "Tipps des Beraters",
        "ag_berater_tipps_desc": "Verbesserungsvorschläge deines Beraters",
        "ag_berater_tipps_tooltip": "Dein Berater hat Vorschläge, was du besser machen kannst.",
    },
    "en": {
        "je_group_berater": "Advisor",
        "je_berater": "The Advisor",
        "je_berater_reason": "Your advisor keeps a constant eye on your country's budget, population, politics, market and diplomacy and tells you where things go wrong and what you can do about it. Critical problems and warnings also show up live in the alert bar at the top.\\n\\nSpecific instructions are one click away: the #bold construction plan#! tells you what to build in which state, the #bold law plan#! which laws to pass next.",
        "je_berater_status_kopf": "Current assessment:",
        "je_berater_status_alles_gut": "\\nNo problems found. Keep it up!",
        "berater_knopf_bericht": "Situation Report",
        "berater_knopf_bericht_desc": "Your advisor sums up all findings with advice and names the affected states and interest groups.",
        "berater_knopf_bauplan": "Construction Plan",
        "berater_knopf_bauplan_desc": "Your advisor tells you which buildings to build in which state.",
        "berater_knopf_gesetzesplan": "Law Plan",
        "berater_knopf_gesetzesplan_desc": "Your advisor recommends your next laws and tells you whether your government backs them.",
        "berater_knopf_jahresbericht_an": "Yearly report: on",
        "berater_knopf_jahresbericht_aus": "Yearly report: off",
        "berater_knopf_jahresbericht_desc": "Turns the automatic yearly situation report on or off.",
        "berater_knopf_krisen_an": "Crisis warnings: on",
        "berater_knopf_krisen_aus": "Crisis warnings: off",
        "berater_knopf_krisen_desc": "Turns the popup warning for critical problems on or off. It appears at most every six months.",
        "berater.1.t": "The Advisor's Situation Report",
        "berater.1.d": "Your Excellency, here is my assessment of our country's situation.",
        "berater.1.f": "“To govern is to foresee.”",
        "berater.1.a": "Thank you, I will see to it.",
        "berater.2.t": "The Advisor Sounds the Alarm",
        "berater.2.d": "Your Excellency, forgive the interruption, but this cannot wait:",
        "berater.2.f": "Critical problems are also shown live in the alert bar. This warning appears at most every six months.",
        "berater.2.a": "Understood.",
        "berater.2.b": "Show me the full situation report.",
        "berater.2.c": "No more crisis warnings.",
        "berater.3.t": "The Advisor's Construction Plan",
        "berater.3.d": "Your Excellency, these projects would help our country most right now. For each one I picked the state where the building is possible and the most workers are available.",
        "berater.3.f": "Prices and states reflect the moment the plan was made. Request a new one from the journal at any time.",
        "berater.3.a": "I will queue the construction.",
        "berater.4.t": "The Advisor's Law Plan",
        "berater.4.d": "Your Excellency, these are the reforms I would pursue next.",
        "berater.4.f": "A law passes more easily when powerful interest groups in the government support it.",
        "berater.4.a": "I will set it in motion.",
        "berater_zeige_lagebericht": "Show me the situation report.",
        "berater_zeige_bauplan": "Show me the construction plan.",
        "berater_zeige_gesetzesplan": "Show me the law plan.",
        "berater_bericht_kopf_kritisch": "\\n\\n#bold CRITICAL PROBLEMS#!",
        "berater_bericht_kopf_warnung": "\\n\\n#bold WARNINGS#!",
        "berater_bericht_kopf_tipp": "\\n\\n#bold TIPS#!",
        "berater_bericht_alles_gut": "\\n\\nI see no problems at the moment. Our country is in good shape, Your Excellency.",
        "berater_bericht_rat": "Advice",
        "berater_bericht_hinweis_plaene": "\\n\\nWhat exactly to build where and which laws to pass is in the #bold construction plan#! and the #bold law plan#!.",
        "berater_warnung_aktion": "More in the journal under “The Advisor”.",
        "berater_bauplan_kopf_gueter": "\\n\\n#bold EXPENSIVE GOODS – PRODUCE THEM YOURSELF#!",
        "berater_bauplan_kopf_infrastruktur": "\\n\\n#bold INFRASTRUCTURE#!",
        "berater_bauplan_kopf_staat": "\\n\\n#bold ADMINISTRATION AND CONSTRUCTION#!",
        "berater_bauplan_infra": "\\n• #bold {STAAT}#! needs more infrastructure than it has, which holds back every building there. Recommended: #bold {BAHN}#!, on the coast also #bold {HAFEN}#!.",
        "berater_bauplan_verwaltung": "\\n• Your bureaucracy is insufficient. Recommended: #bold {VERWALTUNG}#! in #bold {STAAT}#!.",
        "berater_bauplan_bausektor": "\\n• Your construction queue is long and your budget is in surplus, so more construction capacity pays off. Recommended: #bold {BAUSEKTOR}#! in #bold {STAAT}#!.",
        "berater_bauplan_gut": "\\n• #bold {GUT}#! costs {PREIS} above its base price. Recommended: #bold {GEBAEUDE}#! in #bold {STAAT}#!.",
        "berater_bauplan_gut_kein_ort": "\\n• #bold {GUT}#! costs {PREIS} above its base price, but none of your states can host #bold {GEBAEUDE}#!. Secure imports through trade routes.",
        "berater_bauplan_nichts": "\\n\\nNo construction is urgent right now. Prices are reasonable and infrastructure is sufficient. Invest in construction sectors, universities or the industry your country does best.",
        "berater_gesetzplan_aktuell": "\\n\\n#bold IN PROGRESS#!\\n• You are enacting #bold {GESETZ}#!. See it through before starting a new law.",
        "berater_gesetzplan_kopf_empfehlung": "\\n\\n#bold RECOMMENDATIONS#!",
        "berater_gesetzplan_kopf_regierung": "\\n\\n#bold BACKED BY YOUR GOVERNMENT#!\\nYou can introduce these laws now without any governing party opposing them:",
        "berater_gesetzplan_unterstuetzt": " #G Your government backs this.#!",
        "berater_gesetzplan_umstritten": " #Y Your government lacks support for this: bring in interest groups that favor the law.#!",
        "berater_gesetzplan_empfehlung": "\\n• Enact #bold {GESETZ}#!. {GRUND}",
        "berater_gesetzplan_regierung": "\\n• #bold {GESETZ}#!",
        "berater_gesetzplan_nichts": "\\n\\nI have no law to recommend right now. Your laws fit the situation, or the next reforms have not been researched yet.",
        "berater_gesetzplan_warten": "\\n\\nOnce the current law has passed, I can recommend more.",
        "berater_detail_einleitung": "\\n",
        "ag_berater_tipps_name": "Advisor's Tips",
        "ag_berater_tipps_desc": "Suggestions from your advisor",
        "ag_berater_tipps_tooltip": "Your advisor has suggestions on what you could do better.",
    },
}


# ---------------------------------------------------------------- Hilfsfunktionen

def einruecken(text, tiefe):
    """Skriptschnipsel aus der Tabelle (4 Leerzeichen je Ebene) mit Tabs auf `tiefe` einrücken."""
    zeilen = textwrap.dedent(text).strip().splitlines()
    zeilen = [re.sub(r"^( {4})+", lambda m: "\t" * (len(m.group(0)) // 4), z) for z in zeilen]
    return "\n".join("\t" * tiefe + z for z in zeilen)


def nach_stufe(stufe):
    return [e for e in RATSCHLAEGE if e["stufe"] == stufe]


def staat(scope):
    return f"[SCOPE.sState('{scope}').GetName]"


def gebaeude(schluessel):
    return f"[GetBuildingType('{schluessel}').GetName]"


def gesetz(scope):
    return f"[SCOPE.sLaw('{scope}').GetName]"


def ig(scope):
    return f"[SCOPE.gsInterestGroup('{scope}').GetName]"


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


def pruefe_tabellen():
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
        if "detail" in e:
            d = e["detail"]
            if d["typ"] not in ("state", "ig") or "{NAME}" not in d["de"] or "{NAME}" not in d["en"]:
                sys.exit(f"{k}: Detail unvollständig")
        gesehen.add(k)
    gueter = [g[0] for g in GUETER]
    if len(set(gueter)) != len(gueter):
        sys.exit("Gut doppelt in GUETER")
    gesetze = [g["schluessel"] for g in GESETZE]
    if len(set(gesetze)) != len(gesetze):
        sys.exit("Schlüssel doppelt in GESETZE")
    for g in GESETZE:
        if not g["von"] or not g["nach"]:
            sys.exit(f"{g['schluessel']}: von/nach leer")


# ---------------------------------------------------------------- Trigger und Werte

def scripted_triggers():
    teile = ["# Jede Prüfung des Beraters als eigener Trigger im Länder-Scope: berater_problem_<schluessel> = yes\n"]
    for e in RATSCHLAEGE:
        teile.append(f"berater_problem_{e['schluessel']} = {{\n{einruecken(e['bedingung'], 1)}\n}}\n")

    def sammel(name, eintraege, kommentar):
        oder = "\n".join(f"\t\tberater_problem_{e['schluessel']} = yes" for e in eintraege)
        return f"# {kommentar}\n{name} = {{\n\tOR = {{\n{oder}\n\t}}\n}}\n"

    teile.append(sammel("berater_hat_problem", RATSCHLAEGE, "Irgendein Befund liegt vor"))
    for stufe in STUFEN:
        teile.append(sammel(f"berater_hat_problem_{stufe}", nach_stufe(stufe), f"Mindestens ein Befund der Stufe „{stufe}“"))

    teile.append("""# Staats-Scope: eigener, eingegliederter Staat, in dem der Bauplan etwas vorschlagen darf
berater_bauort_geeignet = {
\tis_incorporated = yes
}
""")
    teile.append("""# Gesetz-Scope: kann jetzt eingebracht werden und keine Regierungspartei ist dagegen
berater_gesetz_unterstuetzt = {
\tcan_be_enacted = yes
\tis_reasonable_law_for_petition = yes
}
""")
    for g in GESETZE:
        von = "\n".join(f"\t\thas_law_or_variant = law_type:{law}" for law in g["von"])
        nach = "\n".join(f"\t\t\ttype = law_type:{law}" for law in g["nach"])
        extra = f"\n{einruecken(g['bedingung'], 1)}" if g["bedingung"].strip() else ""
        teile.append(
            f"# Gesetzesempfehlung „{g['schluessel']}“ (Länder-Scope)\n"
            f"berater_gesetz_{g['schluessel']} = {{\n"
            f"\tOR = {{\n{von}\n\t}}\n"
            f"\tany_law = {{\n"
            f"\t\tcan_be_enacted = yes\n"
            f"\t\tOR = {{\n{nach}\n\t\t}}\n"
            f"\t}}{extra}\n"
            f"}}\n"
        )
    return "\n".join(teile)


def script_values():
    teile = ["""# Wöchentliche Einnahmen minus Ausgaben des Staates
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

# Staats-Scope: ungefähre Zahl der Arbeitslosen
berater_arbeitslose = {
\tvalue = state_population
\tmultiply = state_unemployment_rate
}

# Staats-Scope: Eignung als Bauort. Große Staaten mit vielen Arbeitslosen zuerst,
# Staaten mit überlasteter Infrastruktur nur halb so gut.
berater_staat_eignung = {
\tvalue = state_unemployment_rate
\tadd = 0.1
\tmultiply = state_population
\tif = {
\t\tlimit = { infrastructure_usage > infrastructure }
\t\tmultiply = 0.5
\t}
}

# Staats-Scope: wie weit die Infrastruktur überlastet ist
berater_infra_defizit = {
\tvalue = infrastructure_usage
\tsubtract = infrastructure
}

# Interessengruppen-Scope: Unmut (je höher, desto wütender)
berater_ig_unmut = {
\tvalue = ig_approval
\tmultiply = -1
}
"""]
    teile.append("# Preisaufschlag eines Gutes im eigenen Markt gegenüber dem Grundpreis (0,25 = 25 % teurer)")
    for g, *_ in GUETER:
        teile.append(
            f"berater_preis_{g} = {{\n"
            f"\tvalue = 0\n"
            f"\tmarket = {{\n"
            f"\t\tmg:{g} = {{\n"
            f"\t\t\tadd = market_goods_pricier\n"
            f"\t\t}}\n"
            f"\t}}\n"
            f"\tmin = 0\n"
            f"}}\n"
        )
    teile.append("# Verbrauch eines Gutes im eigenen Markt (0 = niemand braucht es, dann kein Bauvorschlag)")
    for g, *_ in GUETER:
        teile.append(
            f"berater_bedarf_{g} = {{\n"
            f"\tvalue = 0\n"
            f"\tmarket = {{\n"
            f"\t\tmg:{g} = {{\n"
            f"\t\t\tadd = market_goods_consumption\n"
            f"\t\t}}\n"
            f"\t}}\n"
            f"}}\n"
        )
    return "\n".join(teile)


# ---------------------------------------------------------------- Warnungen, Journal, Knöpfe

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
\tscripted_button = berater_knopf_bauplan
\tscripted_button = berater_knopf_gesetzesplan
\tscripted_button = berater_knopf_jahresbericht
\tscripted_button = berater_knopf_krisen
}}
"""


def ereignis_knopf(name, ereignis):
    return f"""{name} = {{
\tname = {name}
\tdesc = {name}_desc
\tvisible = {{ always = yes }}
\tpossible = {{ always = yes }}
\teffect = {{
\t\ttrigger_event = {{ id = {ereignis} popup = yes }}
\t}}
\tai_chance = {{
\t\tvalue = 0
\t}}
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
    return "\n".join([
        "# Knöpfe im Journal des Beraters\n",
        ereignis_knopf("berater_knopf_bericht", "berater.1"),
        ereignis_knopf("berater_knopf_bauplan", "berater.3"),
        ereignis_knopf("berater_knopf_gesetzesplan", "berater.4"),
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

# Jährlicher Lagebericht
berater_jaehrlich = {
\ttrigger = {
\t\tis_player = yes
\t\tNOT = { has_variable = berater_kein_jahresbericht }
\t}
\tevents = { berater.1 }
}
"""


# ---------------------------------------------------------------- Ereignisse

def td(desc, trigger, t):
    """Ein triggered_desc, eingerückt mit `t` Tabs; `trigger` ist eine Liste von Zeilen."""
    innen = "\n".join(f"{t}\t\t{z}" for z in trigger)
    return f"{t}triggered_desc = {{\n{t}\tdesc = {desc}\n{t}\ttrigger = {{\n{innen}\n{t}\t}}\n{t}}}"


def bericht_desc(stufen, t):
    """Lagebericht: Abschnitt je Stufe, jeder Befund mit optionalem Detail (Staat, Interessengruppe)."""
    teile = []
    for stufe in stufen:
        eintraege = nach_stufe(stufe)
        if not eintraege:
            continue
        teile.append(td(f"berater_bericht_kopf_{stufe}", [f"berater_hat_problem_{stufe} = yes"], t))
        for e in eintraege:
            k = e["schluessel"]
            teile.append(td(f"berater_bericht_{k}", [f"berater_problem_{k} = yes"], t))
            if "detail" in e:
                teile.append(td(f"berater_bericht_{k}_detail",
                                [f"berater_problem_{k} = yes", f"exists = scope:{e['detail']['scope']}"], t))
    return "\n".join(teile)


def ereignis(nr, titel_desc, desc, trigger, immediate, optionen, flavor=True):
    video, symbol = EREIGNIS_BILD[nr]
    opt = []
    for i, (name, effekt) in enumerate(optionen):
        zeilen = [f"\t\tname = {name}"]
        if i == 0:
            zeilen.append("\t\tdefault_option = yes")
        if effekt:
            zeilen.append(f"\t\t{effekt}")
        opt.append("\toption = {\n" + "\n".join(zeilen) + "\n\t}")
    imm = f"\n\timmediate = {{\n{immediate}\n\t}}\n" if immediate else ""
    fl = f"\tflavor = berater.{nr}.f\n" if flavor else ""
    trig = "\n".join(f"\t\t{z}" for z in trigger)
    return f"""{titel_desc}
berater.{nr} = {{
\ttype = country_event
\ttitle = berater.{nr}.t
\tdesc = {{
\t\tdesc = berater.{nr}.d
{desc}
\t}}
{fl}\tevent_image = {{
\t\tvideo = "{video}"
\t}}
\ticon = "gfx/interface/icons/event_icons/{symbol}.dds"
\tduration = 3

\ttrigger = {{
{trig}
\t}}
{imm}
{chr(10).join(opt)}
}}
"""


def zeige(nr):
    return f"trigger_event = {{ id = berater.{nr} popup = yes }}"


def lagebericht():
    details = []
    for e in RATSCHLAEGE:
        if "detail" in e:
            details.append(
                f"\t\tif = {{\n"
                f"\t\t\tlimit = {{ berater_problem_{e['schluessel']} = yes }}\n"
                f"{einruecken(e['detail']['effekt'], 3)}\n"
                f"\t\t}}"
            )
    desc = "\n".join([
        bericht_desc(STUFEN, "\t\t"),
        td("berater_bericht_alles_gut", ["berater_hat_problem = no"], "\t\t"),
        "\t\tdesc = berater_bericht_hinweis_plaene",
    ])
    return ereignis(
        1, "# Lagebericht: alle Befunde mit Ratschlägen; über den Journal-Knopf oder einmal im Jahr",
        desc, ["is_player = yes"], "\n".join(details),
        [("berater.1.a", ""), ("berater_zeige_bauplan", zeige(3)), ("berater_zeige_gesetzesplan", zeige(4))],
    )


def krisenwarnung():
    return ereignis(
        2, "# Krisenwarnung: nur akute Probleme, ausgelöst von berater_monatlich",
        bericht_desc(["kritisch"], "\t\t"),
        ["is_player = yes", "berater_hat_problem_kritisch = yes"], "",
        [("berater.2.a", ""), ("berater.2.b", zeige(1)), ("berater.2.c", "set_variable = berater_keine_krisenwarnungen")],
    )


def ort_suche(gebaeude_schluessel, scope, t, sortierung="berater_staat_eignung", zusatz=()):
    limit = "\n".join(f"{t}\t\t{z}" for z in ["berater_bauort_geeignet = yes", f"can_construct_building = {gebaeude_schluessel}", *zusatz])
    return (
        f"{t}ordered_scope_state = {{\n"
        f"{t}\tlimit = {{\n{limit}\n{t}\t}}\n"
        f"{t}\torder_by = {sortierung}\n"
        f"{t}\tmax = 1\n"
        f"{t}\tsave_scope_as = {scope}\n"
        f"{t}}}"
    )


def bauplan():
    imm = ["\t\tset_local_variable = {\n\t\t\tname = berater_anzahl\n\t\t\tvalue = 0\n\t\t}"]
    for g, _, _, gebaeude_liste in GUETER:
        suche = [ort_suche(gebaeude_liste[0], f"berater_ort_{g}_1", "\t\t\t")]
        for i, b in enumerate(gebaeude_liste[1:], 2):
            vorher = "\n".join(f"\t\t\t\t\texists = scope:berater_ort_{g}_{j}" for j in range(1, i))
            suche.append(
                f"\t\t\tif = {{\n"
                f"\t\t\t\tlimit = {{\n\t\t\t\t\tNOR = {{\n{vorher.replace(chr(9) * 5, chr(9) * 6)}\n\t\t\t\t\t}}\n\t\t\t\t}}\n"
                f"{ort_suche(b, f'berater_ort_{g}_{i}', chr(9) * 4)}\n"
                f"\t\t\t}}"
            )
        imm.append(
            f"\t\tif = {{\n"
            f"\t\t\tlimit = {{\n"
            f"\t\t\t\tlocal_var:berater_anzahl < {MAX_GUETER}\n"
            f"\t\t\t\tberater_preis_{g} >= {PREIS_SCHWELLE}\n"
            f"\t\t\t\tberater_bedarf_{g} > 0\n"
            f"\t\t\t}}\n"
            f"\t\t\tchange_local_variable = {{\n\t\t\t\tname = berater_anzahl\n\t\t\t\tadd = 1\n\t\t\t}}\n"
            f"\t\t\tsave_scope_as = berater_bau_{g}\n"
            + "\n".join(suche) + "\n"
            f"\t\t}}"
        )
    # Infrastruktur: die zwei am stärksten überlasteten Staaten
    imm.append(
        "\t\tordered_scope_state = {\n"
        "\t\t\tlimit = {\n\t\t\t\tberater_bauort_geeignet = yes\n\t\t\t\tinfrastructure_usage > infrastructure\n\t\t\t}\n"
        "\t\t\torder_by = berater_infra_defizit\n\t\t\tmax = 1\n\t\t\tsave_scope_as = berater_infra_1\n\t\t}\n"
        "\t\tif = {\n\t\t\tlimit = { exists = scope:berater_infra_1 }\n"
        "\t\t\tordered_scope_state = {\n"
        "\t\t\t\tlimit = {\n\t\t\t\t\tberater_bauort_geeignet = yes\n\t\t\t\t\tinfrastructure_usage > infrastructure\n"
        "\t\t\t\t\tNOT = { this = scope:berater_infra_1 }\n\t\t\t\t}\n"
        "\t\t\t\torder_by = berater_infra_defizit\n\t\t\t\tmax = 1\n\t\t\t\tsave_scope_as = berater_infra_2\n\t\t\t}\n\t\t}"
    )
    imm.append(
        "\t\tif = {\n\t\t\tlimit = { bureaucracy < 0 }\n"
        + ort_suche("building_government_administration", "berater_ort_verwaltung", "\t\t\t", "state_population") +
        "\n\t\t}"
    )
    imm.append(
        "\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tconstruction_queue_government_duration > 52\n"
        "\t\t\t\tberater_wochenbilanz > 0\n\t\t\t\tscaled_debt < 0.5\n\t\t\t}\n"
        + ort_suche("building_construction_sector", "berater_ort_bausektor", "\t\t\t", "state_population") +
        "\n\t\t}"
    )

    t = "\t\t"
    desc = []
    alle_gueter = [f"exists = scope:berater_bau_{g}" for g, *_ in GUETER]
    desc.append(td("berater_bauplan_kopf_gueter", ["OR = {"] + [f"\t{z}" for z in alle_gueter] + ["}"], t))
    for g, _, _, gebaeude_liste in GUETER:
        orte = [f"berater_ort_{g}_{i}" for i in range(1, len(gebaeude_liste) + 1)]
        for i, ort in enumerate(orte, 1):
            vorher = [f"\t\texists = scope:{o}" for o in orte[:i - 1]]
            bedingung = [f"exists = scope:berater_bau_{g}", f"exists = scope:{ort}"]
            if vorher:
                bedingung += ["NOR = {"] + [z[1:] for z in vorher] + ["}"]
            desc.append(td(f"berater_bauplan_{g}_{i}", bedingung, t))
        desc.append(td(f"berater_bauplan_{g}_kein_ort",
                       [f"exists = scope:berater_bau_{g}", "NOR = {"] + [f"\texists = scope:{o}" for o in orte] + ["}"], t))
    desc.append(td("berater_bauplan_kopf_infrastruktur", ["exists = scope:berater_infra_1"], t))
    desc.append(td("berater_bauplan_infra_1", ["exists = scope:berater_infra_1"], t))
    desc.append(td("berater_bauplan_infra_2", ["exists = scope:berater_infra_2"], t))
    desc.append(td("berater_bauplan_kopf_staat",
                   ["OR = {", "\texists = scope:berater_ort_verwaltung", "\texists = scope:berater_ort_bausektor", "}"], t))
    desc.append(td("berater_bauplan_verwaltung", ["exists = scope:berater_ort_verwaltung"], t))
    desc.append(td("berater_bauplan_bausektor", ["exists = scope:berater_ort_bausektor"], t))
    alles = alle_gueter + ["exists = scope:berater_infra_1", "exists = scope:berater_ort_verwaltung",
                           "exists = scope:berater_ort_bausektor"]
    desc.append(td("berater_bauplan_nichts", ["NOR = {"] + [f"\t{z}" for z in alles] + ["}"], t))

    return ereignis(
        3, "# Bauplan: was in welchem Staat gebaut werden sollte",
        "\n".join(desc), ["is_player = yes"], "\n".join(imm),
        [("berater.3.a", ""), ("berater_zeige_gesetzesplan", zeige(4)), ("berater_zeige_lagebericht", zeige(1))],
    )


def gesetzesplan():
    imm = [
        "\t\tset_local_variable = {\n\t\t\tname = berater_anzahl\n\t\t\tvalue = 0\n\t\t}",
        "\t\tif = {\n\t\t\tlimit = { enacting_any_law = yes }\n"
        "\t\t\tcurrently_enacting_law = {\n\t\t\t\tsave_scope_as = berater_gesetz_aktuell\n\t\t\t}\n\t\t}",
    ]
    for g in GESETZE:
        k = g["schluessel"]
        ziel = f"berater_gesetz_{k}_ziel"
        wahl = []
        for law in g["nach"]:
            wahl.append(
                f"\t\t\tif = {{\n"
                f"\t\t\t\tlimit = {{\n"
                f"\t\t\t\t\tNOT = {{ exists = scope:{ziel} }}\n"
                f"\t\t\t\t\tany_law = {{\n\t\t\t\t\t\ttype = law_type:{law}\n\t\t\t\t\t\tcan_be_enacted = yes\n\t\t\t\t\t}}\n"
                f"\t\t\t\t}}\n"
                f"\t\t\t\trandom_law = {{\n"
                f"\t\t\t\t\tlimit = {{ type = law_type:{law} }}\n"
                f"\t\t\t\t\tsave_scope_as = {ziel}\n"
                f"\t\t\t\t}}\n"
                f"\t\t\t}}"
            )
        imm.append(
            f"\t\tif = {{\n"
            f"\t\t\tlimit = {{\n"
            f"\t\t\t\tlocal_var:berater_anzahl < {MAX_GESETZE}\n"
            f"\t\t\t\tberater_gesetz_{k} = yes\n"
            f"\t\t\t}}\n"
            f"\t\t\tchange_local_variable = {{\n\t\t\t\tname = berater_anzahl\n\t\t\t\tadd = 1\n\t\t\t}}\n"
            + "\n".join(wahl) + "\n"
            f"\t\t}}"
        )
    # Weitere Gesetze, die die Regierung mitträgt, ohne die schon empfohlenen
    ausschluss = []
    for g in GESETZE:
        z = f"berater_gesetz_{g['schluessel']}_ziel"
        ausschluss.append(
            f"trigger_if = {{\n\tlimit = {{ exists = scope:{z} }}\n\tNOT = {{ this = scope:{z} }}\n}}"
        )
    for i in range(1, ANZAHL_REGIERUNGSGESETZE + 1):
        weitere = list(ausschluss) + [f"NOT = {{ this = scope:berater_gesetz_reg_{j} }}" for j in range(1, i)]
        limit = "\n".join(einruecken(z, 5 if i > 1 else 4) for z in ["berater_gesetz_unterstuetzt = yes", *weitere])
        if i == 1:
            imm.append(f"\t\trandom_law = {{\n\t\t\tlimit = {{\n{limit}\n\t\t\t}}\n\t\t\tsave_scope_as = berater_gesetz_reg_1\n\t\t}}")
        else:
            imm.append(
                f"\t\tif = {{\n\t\t\tlimit = {{ exists = scope:berater_gesetz_reg_{i - 1} }}\n"
                f"\t\t\trandom_law = {{\n\t\t\t\tlimit = {{\n{limit}\n\t\t\t\t}}\n"
                f"\t\t\t\tsave_scope_as = berater_gesetz_reg_{i}\n\t\t\t}}\n\t\t}}"
            )

    t = "\t\t"
    ziele = [f"exists = scope:berater_gesetz_{g['schluessel']}_ziel" for g in GESETZE]
    desc = [td("berater_gesetzplan_aktuell", ["exists = scope:berater_gesetz_aktuell"], t)]
    desc.append(td("berater_gesetzplan_kopf_empfehlung", ["OR = {"] + [f"\t{z}" for z in ziele] + ["}"], t))
    for g in GESETZE:
        z = f"berater_gesetz_{g['schluessel']}_ziel"
        desc.append(td(f"berater_gesetzplan_{g['schluessel']}", [f"exists = scope:{z}"], t))
        desc.append(td("berater_gesetzplan_unterstuetzt",
                       [f"exists = scope:{z}", f"scope:{z} = {{ is_reasonable_law_for_petition = yes }}"], t))
        desc.append(td("berater_gesetzplan_umstritten",
                       [f"exists = scope:{z}", f"scope:{z} = {{ is_reasonable_law_for_petition = no }}"], t))
    desc.append(td("berater_gesetzplan_kopf_regierung", ["exists = scope:berater_gesetz_reg_1"], t))
    for i in range(1, ANZAHL_REGIERUNGSGESETZE + 1):
        desc.append(td(f"berater_gesetzplan_regierung_{i}", [f"exists = scope:berater_gesetz_reg_{i}"], t))
    nichts = ziele + ["exists = scope:berater_gesetz_reg_1"]
    desc.append(td("berater_gesetzplan_nichts", ["NOR = {"] + [f"\t{z}" for z in nichts] + ["}"], t))
    desc.append(td("berater_gesetzplan_warten",
                   ["exists = scope:berater_gesetz_aktuell", "NOR = {"] + [f"\t{z}" for z in nichts] + ["}"], t))

    return ereignis(
        4, "# Gesetzesplan: welche Gesetze als Nächstes und ob die Regierung sie mitträgt",
        "\n".join(desc), ["is_player = yes"], "\n".join(imm),
        [("berater.4.a", ""), ("berater_zeige_bauplan", zeige(3)), ("berater_zeige_lagebericht", zeige(1))],
    )


def events():
    return "namespace = berater\n\n" + "\n".join([lagebericht(), krisenwarnung(), bauplan(), gesetzesplan()])


# ---------------------------------------------------------------- Lokalisierung

def loc_text(text):
    # Gerade Anführungszeichen beenden in Paradox-Lokalisierung den Text; typografische verwenden
    if '"' in text:
        sys.exit(f"Gerades Anführungszeichen im Text: {text!r}")
    return text


def lokalisierung(sprache):
    texte = dict(TEXTE[sprache])
    stufen = STUFEN_TEXT[sprache]
    rat = texte["berater_bericht_rat"]
    for e in RATSCHLAEGE:
        k = e["schluessel"]
        titel, befund, ratschlag = e[sprache]
        texte[f"je_berater_status_{k}"] = f"\\n• {stufen[e['stufe']]}: {titel}"
        texte[f"berater_bericht_{k}"] = f"\\n\\n• #bold {titel}#!\\n{befund}\\n{rat}: {ratschlag}"
        if "detail" in e:
            d = e["detail"]
            name = staat(d["scope"]) if d["typ"] == "state" else ig(d["scope"])
            texte[f"berater_bericht_{k}_detail"] = "\\n" + d[sprache].replace("{NAME}", f"#bold {name}#!")
        if e["warnung"]:
            texte[f"alert_berater_{k}_name"] = titel
            texte[f"alert_berater_{k}_desc"] = befund
            texte[f"alert_berater_{k}_hint"] = f"{rat}: {ratschlag}"
            texte[f"alert_berater_{k}_action"] = texte["berater_warnung_aktion"]
            texte[f"berater_{k}_setting_name"] = f"{texte['je_berater']}: {titel}"

    gut_vorlage = texte.pop("berater_bauplan_gut")
    kein_ort_vorlage = texte.pop("berater_bauplan_gut_kein_ort")
    for g, de, en, gebaeude_liste in GUETER:
        name = de if sprache == "de" else en
        preis = f"#bold [ROOT.GetCountry.MakeScope.ScriptValue('berater_preis_{g}')|%0]#!"
        for i, b in enumerate(gebaeude_liste, 1):
            texte[f"berater_bauplan_{g}_{i}"] = (
                gut_vorlage.replace("{GUT}", name).replace("{PREIS}", preis)
                .replace("{GEBAEUDE}", gebaeude(b)).replace("{STAAT}", staat(f"berater_ort_{g}_{i}"))
            )
        texte[f"berater_bauplan_{g}_kein_ort"] = (
            kein_ort_vorlage.replace("{GUT}", name).replace("{PREIS}", preis)
            .replace("{GEBAEUDE}", gebaeude(gebaeude_liste[0]))
        )
    infra = texte.pop("berater_bauplan_infra")
    for i in (1, 2):
        texte[f"berater_bauplan_infra_{i}"] = (
            infra.replace("{STAAT}", staat(f"berater_infra_{i}"))
            .replace("{BAHN}", gebaeude("building_railway")).replace("{HAFEN}", gebaeude("building_port"))
        )
    texte["berater_bauplan_verwaltung"] = (
        texte["berater_bauplan_verwaltung"].replace("{VERWALTUNG}", gebaeude("building_government_administration"))
        .replace("{STAAT}", staat("berater_ort_verwaltung"))
    )
    texte["berater_bauplan_bausektor"] = (
        texte["berater_bauplan_bausektor"].replace("{BAUSEKTOR}", gebaeude("building_construction_sector"))
        .replace("{STAAT}", staat("berater_ort_bausektor"))
    )

    texte["berater_gesetzplan_aktuell"] = texte["berater_gesetzplan_aktuell"].replace("{GESETZ}", gesetz("berater_gesetz_aktuell"))
    empfehlung = texte.pop("berater_gesetzplan_empfehlung")
    for g in GESETZE:
        k = g["schluessel"]
        texte[f"berater_gesetzplan_{k}"] = (
            empfehlung.replace("{GESETZ}", gesetz(f"berater_gesetz_{k}_ziel")).replace("{GRUND}", g[sprache])
        )
    regierung = texte.pop("berater_gesetzplan_regierung")
    for i in range(1, ANZAHL_REGIERUNGSGESETZE + 1):
        texte[f"berater_gesetzplan_regierung_{i}"] = regierung.replace("{GESETZ}", gesetz(f"berater_gesetz_reg_{i}"))

    for k, v in texte.items():
        if re.search(r"\{[A-Z]+\}", v):
            sys.exit(f"Platzhalter nicht ersetzt in {k}: {v!r}")
    return texte


def schreibe_lokalisierung():
    for sprache in SPRACHEN:
        texte = lokalisierung("de" if sprache == "german" else "en")
        zeilen = [f"l_{sprache}:"]
        zeilen += [f' {k}: "{loc_text(v)}"' for k, v in texte.items()]
        schreibe(f"localization/{sprache}/berater_l_{sprache}.yml", "\n".join(zeilen) + "\n")


# ---------------------------------------------------------------- Hauptprogramm

def main():
    pruefe_tabellen()
    print(f"{len(RATSCHLAEGE)} Ratschläge, {len(GUETER)} Güter, {len(GESETZE)} Gesetzesempfehlungen, schreibe:")
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
