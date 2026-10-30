# Der Berater – Live-Ratschläge für Victoria 3

Eine Mod für Victoria 3, die dein Land während des Spiels laufend analysiert und dir sagt, was du besser machen kannst.

## Was die Mod macht

| Funktion | Wann | Wo |
|---|---|---|
| **Live-Warnungen** | sofort, solange ein Problem besteht | Warnleiste oben (rot: akut, gelb: Warnung, grün: Tipps, zusammengefasst) |
| **Journal „Der Berater“** | immer aktiv, aktualisiert sich laufend | Journal, Gruppe „Berater“: Liste aller aktuellen Befunde |
| **Lagebericht** | auf Knopfdruck im Journal und einmal im Jahr | jeder Befund mit Ratschlag, dazu der am stärksten betroffene Staat bzw. die wütendste Interessengruppe |
| **Bauplan** | auf Knopfdruck im Journal | welches Gebäude in welchem Staat gebaut werden sollte |
| **Gesetzesplan** | auf Knopfdruck im Journal | welche Gesetze als Nächstes, warum, und ob die Regierung sie mitträgt |
| **Krisenwarnung** | monatliche Prüfung; höchstens alle 6 Monate | Popup, wenn ein akutes Problem vorliegt |

Im Journal lassen sich Jahresbericht und Krisenwarnungen ein- und ausschalten.

### Bauplan

- **Teure Güter selbst herstellen:** Für bis zu 5 Güter, die im eigenen Markt mindestens 20 % über dem Grundpreis liegen und gebraucht werden, nennt der Berater das passende Gebäude (z. B. Kohlebergwerk, Stahlwerk, Weizenfarm) und den besten eigenen Staat dafür. Bester Staat heißt: Das Gebäude ist dort baubar (Ressourcen, Technologie), und es gibt viele Einwohner und Arbeitslose; Staaten mit überlasteter Infrastruktur zählen nur halb. Ist das Gebäude nirgends möglich, rät er zu Importen.
- **Infrastruktur:** die zwei Staaten mit der am stärksten überlasteten Infrastruktur, mit Eisenbahn oder Hafen als Empfehlung.
- **Verwaltung:** bei Bürokratie im Minus eine Regierungsverwaltung im passenden Staat.
- **Bausektor:** bei langer Bauwarteschlange und gesundem Haushalt ein weiterer Bausektor.

### Gesetzesplan

- **In Arbeit:** das Gesetz, das gerade verabschiedet wird.
- **Empfehlungen (bis zu 4):** zum Beispiel Pächter statt Leibeigenschaft, Interventionismus statt Traditionalismus, ernannte statt erblicher Beamter, Schulen, Steuerreform; einige nur bei passender Lage (z. B. lockerere Staatsbürgerschaft bei Separatisten oder Unruhe). Nur Gesetze, die du schon einbringen kannst, mit Begründung und dem Hinweis, ob deine Regierung sie mitträgt.
- **Von der Regierung mitgetragen:** bis zu drei weitere Gesetze, die du jetzt einbringen kannst, ohne dass eine Regierungspartei dagegen ist. Einzelne Live-Warnungen schaltest du in den Warnungseinstellungen des Spiels ab (Einträge „Der Berater: …“).

## Was der Berater prüft (27 Befunde)

**Akut:** Staatsbankrott · Schulden über 80 % der Kreditgrenze · revolutionäre Bewegung · Kriegsunterstützung unter null · Paria-Infamie

**Warnungen:** Schulden über 50 % · Haushaltsdefizit bei leeren Reserven · Bürokratie, Autorität oder Einfluss im Minus · Unruhe in Staaten · über 20 % Radikale · mächtige Interessengruppe wütend · Arbeitslosigkeit über 15 % · über 30 % der Bevölkerung unter dem erwarteten Lebensstandard · Güterknappheit im Markt · hohe Infamie · wachsende Separatisten · niedrige Legitimität

**Tipps:** keine Forschung aktiv · leere Bauwarteschlange · Bauwarteschlange über zwei Jahre · Goldreserven fast voll · hohe Steuern trotz gesundem Haushalt · niedrige Alphabetisierung · teure Industriegüter (Kohle, Eisen, Holz, Werkzeuge, Stahl) · kein Gesetz in Arbeit

Einige Befunde (Forschung, Bauwarteschlange leer, Bürokratie/Autorität/Einfluss, Gesetze) erscheinen nur im Journal und im Bericht, weil das Spiel dafür schon eigene Warnungen zeigt.

## Installation

1. Den Inhalt dieses Repositorys in einen Ordner `berater` kopieren, zum Beispiel:
   - Windows: `Dokumente\Paradox Interactive\Victoria 3\mod\berater`
   - Linux: `~/.local/share/Paradox Interactive/Victoria 3/mod/berater`
   - macOS: `~/Documents/Paradox Interactive/Victoria 3/mod/berater`
2. Im Launcher unter „Playsets“ die Mod über „Lokale Mod hinzufügen“ einbinden und aktivieren.
3. Spiel starten (neues Spiel oder Spielstand). Das Journal „Der Berater“ wird automatisch aktiv.

Die Mod verändert keine Spielregeln, nur Anzeigen und Ereignisse. Sie lässt sich daher in laufenden Spielständen ein- und ausschalten und ist mit den meisten anderen Mods verträglich.

## Testen und Fehler melden

Die Mod wurde gegen die aktuelle Liste der Victoria-3-Trigger (CWTools-Konfiguration) geschrieben, aber noch nicht im Spiel getestet. Nach dem ersten Start bitte prüfen:

- Datei `error.log` unter `Dokumente\Paradox Interactive\Victoria 3\logs\` nach `berater` durchsuchen.
- Erscheint das Journal „Der Berater“? Funktionieren die drei Knöpfe?
- Tauchen Warnungen in der Warnleiste auf (z. B. „Industriegüter teuer“ oder „Steuern senkbar“)?
- Nennen Bauplan und Gesetzesplan Staaten, Gebäude und Gesetze mit Namen (und nicht leere Stellen)?

Fehlerzeilen aus der `error.log` als Issue melden, dann lassen sie sich gezielt beheben.

## Aufbau

```
.metadata/metadata.json          Beschreibung für den Launcher
common/scripted_triggers/        die Prüfungen (berater_problem_<name>)
common/script_values/            Hilfswerte (Wochenbilanz, Anteil unter erwartetem Lebensstandard)
common/alert_types/              Live-Warnungen
common/alert_groups/             Gruppe für die Tipps in der Warnleiste
common/journal_entries/          Journal „Der Berater“
common/journal_entry_groups/     Journalgruppe „Berater“
common/scripted_buttons/         Knöpfe im Journal
common/on_actions/               monatliche Krisenprüfung, Jahresbericht
events/berater_events.txt        Lagebericht (berater.1), Krisenwarnung (berater.2),
                                 Bauplan (berater.3), Gesetzesplan (berater.4)
gfx/interface/icons/berater/     Warnsymbole
localization/                    Deutsch; alle anderen Sprachen auf Englisch
werkzeuge/                       Generator (Python)
```

## Ratschläge ändern oder ergänzen

Alle Prüfungen und Texte stehen in zwei Tabellen: `werkzeuge/ratschlaege.py` (Befunde für Warnungen, Journal und Lagebericht) und `werkzeuge/plaene.py` (Güter und Gebäude für den Bauplan, Gesetzesempfehlungen). Danach neu erzeugen:

```bash
python3 werkzeuge/erzeuge_mod.py
```

Der Generator schreibt Trigger, Warnungen, Journal, Ereignisse und Lokalisierung neu und prüft dabei Schlüssel, Texte und Klammern. Die Grafiken (benötigt Pillow) erzeugt `python3 werkzeuge/erzeuge_grafiken.py`.
