"""Die Ratschläge des Beraters: eine Tabelle, aus der erzeuge_mod.py alle Skripte und Texte baut.

Jeder Eintrag beschreibt eine Prüfung im Länder-Scope (ROOT = Spielerland):

    schluessel   Kürzel für Trigger, Warnungen und Lokalisierung (nur a–z und _)
    stufe        "kritisch", "warnung" oder "tipp"
    warnung      True: erscheint live als Warnung in der oberen Leiste.
                 False: nur im Journal und im Bericht (z. B. weil das Spiel selbst
                 schon eine Warnung dafür zeigt).
    bedingung    Victoria-3-Trigger (Länder-Scope); wahr = das Problem liegt vor
    de / en      Titel, Befund und Ratschlag
    detail       optional: benennt im Lagebericht den betroffenen Staat oder die Interessengruppe
                 (scope: gespeicherter Scope, typ: "state" oder "ig", effekt: wählt ihn aus,
                 de/en: Text mit {NAME})

Neue Ratschläge hier eintragen und danach `python3 werkzeuge/erzeuge_mod.py` ausführen.
"""

RATSCHLAEGE = [
    # ------------------------------------------------------------------ kritisch
    {
        "schluessel": "bankrott",
        "stufe": "kritisch",
        "warnung": True,
        "bedingung": """
            in_default = yes
        """,
        "de": (
            "Staatsbankrott",
            "Dein Staat ist zahlungsunfähig. Bauvorhaben stocken, Gehälter fallen aus, und die Interessengruppen verlieren das Vertrauen in die Regierung.",
            "Erhöhe sofort Steuern oder Zölle, senke Beamten- und Militärgehälter, demobilisiere überflüssige Truppen und streiche Subventionen. Stelle unrentable Bauvorhaben zurück, bis die Wochenbilanz wieder positiv ist.",
        ),
        "en": (
            "State Bankruptcy",
            "Your state is in default. Construction stalls, salaries go unpaid and interest groups lose faith in the government.",
            "Raise taxes or tariffs immediately, lower government and military wages, demobilize unneeded troops and cut subsidies. Pause unprofitable construction until your weekly balance is positive again.",
        ),
    },
    {
        "schluessel": "schulden_kritisch",
        "stufe": "kritisch",
        "warnung": True,
        "bedingung": """
            in_default = no
            scaled_debt >= 0.8
        """,
        "de": (
            "Schulden am Limit",
            "Deine Schulden haben über 80 % der Kreditgrenze erreicht. Bei 100 % droht der Staatsbankrott.",
            "Bringe den Haushalt sofort ins Plus: Steuern oder Zölle anheben, Gehälter senken und teure Bauvorhaben zurückstellen. Jeder weitere Kredit verteuert die Zinsen.",
        ),
        "en": (
            "Debt at the Limit",
            "Your debt has passed 80 % of your credit limit. At 100 % you will default.",
            "Get the budget into surplus now: raise taxes or tariffs, lower wages and postpone expensive construction. Every further loan increases your interest payments.",
        ),
    },
    {
        "schluessel": "revolution",
        "stufe": "kritisch",
        "warnung": True,
        "bedingung": """
            any_political_movement = {
                is_revolutionary = yes
            }
        """,
        "de": (
            "Revolution droht",
            "Mindestens eine politische Bewegung ist revolutionär geworden. Sammelt sie genug Unterstützung, bricht ein Bürgerkrieg aus.",
            "Gib der Bewegung nach, indem du ein Gesetz in ihrem Sinn einleitest, oder schwäche sie: unterdrücke die unterstützenden Interessengruppen, hebe den Lebensstandard und brich Gesetzesvorhaben ab, die sie ablehnt. Halte die Armee bereit.",
        ),
        "en": (
            "Revolution Looming",
            "At least one political movement has turned revolutionary. If it gathers enough support, a civil war will break out.",
            "Give in by enacting a law the movement wants, or weaken it: suppress the supporting interest groups, raise the standard of living and drop laws it opposes. Keep your army ready.",
        ),
    },
    {
        "schluessel": "kriegsunterstuetzung",
        "stufe": "kritisch",
        "warnung": True,
        "bedingung": """
            any_scope_war = {
                has_war_support = {
                    target = root
                    value < 0
                }
            }
        """,
        "de": (
            "Kriegsunterstützung im Minus",
            "In mindestens einem Krieg ist die Kriegsunterstützung deines Landes unter null gefallen. Bei -100 musst du kapitulieren.",
            "Biete jetzt einen Frieden mit wenigen Kriegszielen an oder nimm ein vernünftiges Angebot an, bevor du zur Kapitulation gezwungen wirst. Die Besetzung gegnerischer Kriegsziele stabilisiert die eigene Kriegsunterstützung.",
        ),
        "en": (
            "War Support Below Zero",
            "In at least one war your country's war support has dropped below zero. At -100 you will be forced to capitulate.",
            "Offer peace with few war goals now, or accept a reasonable offer, before you are forced to capitulate. Occupying enemy war goals stabilizes your own war support.",
        ),
    },
    {
        "schluessel": "infamie_paria",
        "stufe": "kritisch",
        "warnung": True,
        "bedingung": """
            infamy >= infamy_threshold:pariah
        """,
        "de": (
            "Paria-Staat",
            "Deine Infamie ist so hoch, dass andere Mächte jeden Vorwand nutzen werden, um gegen dich vorzugehen.",
            "Verzichte auf weitere Eroberungen und aggressive Forderungen, bis die Infamie gesunken ist. Suche Verbündete und Verteidigungspakte.",
        ),
        "en": (
            "Pariah State",
            "Your infamy is so high that other powers will use any pretext to move against you.",
            "Stop all further conquests and aggressive demands until your infamy has dropped. Look for allies and defensive pacts.",
        ),
    },
    # ------------------------------------------------------------------ warnung
    {
        "schluessel": "schulden_hoch",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            in_default = no
            scaled_debt >= 0.5
            scaled_debt < 0.8
        """,
        "de": (
            "Hohe Staatsschulden",
            "Deine Schulden betragen mehr als die Hälfte der Kreditgrenze. Die Zinsen belasten den Haushalt immer stärker.",
            "Strebe einen Haushaltsüberschuss an, um die Schulden abzubauen: Steuern maßvoll erhöhen, Ausgaben prüfen und nur Bauvorhaben mit hoher Rendite (Industrie, Bergbau, Eisenbahn) fortsetzen.",
        ),
        "en": (
            "High National Debt",
            "Your debt is more than half of your credit limit. Interest payments weigh ever more heavily on the budget.",
            "Aim for a budget surplus to pay down the debt: raise taxes moderately, review your expenses and only continue high-yield construction (industry, mining, railways).",
        ),
    },
    {
        "schluessel": "defizit",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            in_default = no
            berater_wochenbilanz < 0
            scaled_gold_reserves < 0.25
        """,
        "de": (
            "Haushaltsdefizit",
            "Dein Staat gibt jede Woche mehr aus, als er einnimmt, und die Goldreserven sind fast aufgebraucht. Bald müssen Kredite aufgenommen werden.",
            "Erhöhe Steuern oder Zölle, senke Beamten- oder Militärgehälter oder verringere die Bauausgaben. Prüfe auch teure Gesetze wie Subventionen und Sozialprogramme.",
        ),
        "en": (
            "Budget Deficit",
            "Your state spends more each week than it earns, and your gold reserves are nearly gone. Soon you will have to take on debt.",
            "Raise taxes or tariffs, lower government or military wages, or reduce construction spending. Also review expensive laws such as subsidies and welfare programs.",
        ),
    },
    {
        "schluessel": "buerokratie",
        "stufe": "warnung",
        "warnung": False,
        "bedingung": """
            bureaucracy < 0
        """,
        "de": (
            "Bürokratie im Minus",
            "Du verbrauchst mehr Bürokratie, als deine Verwaltung erzeugt. Das senkt die Steuereinnahmen und verlangsamt die Eingliederung neuer Staaten.",
            "Baue Regierungsverwaltungen in Staaten mit vielen gebildeten Arbeitskräften, stelle Gesetze und Institutionen mit hohem Bürokratieverbrauch zurück oder wähle bessere Produktionsmethoden für die Verwaltungen.",
        ),
        "en": (
            "Negative Bureaucracy",
            "You use more bureaucracy than your administration produces. This lowers tax income and slows down the incorporation of new states.",
            "Build government administrations in states with many educated workers, postpone laws and institutions with high bureaucracy costs, or choose better production methods for your administrations.",
        ),
    },
    {
        "schluessel": "autoritaet",
        "stufe": "warnung",
        "warnung": False,
        "bedingung": """
            authority < 0
        """,
        "de": (
            "Autorität im Minus",
            "Erlasse, Zölle und Gesetze verbrauchen mehr Autorität, als du hast. Dadurch verlieren alle Autoritätsausgaben an Wirkung.",
            "Hebe weniger wichtige Erlasse auf, beschränke Zölle und Handelsvorgaben auf wenige Güter oder stärke die Autorität über Gesetze und Technologien.",
        ),
        "en": (
            "Negative Authority",
            "Decrees, tariffs and laws consume more authority than you have. Every use of authority loses effectiveness as a result.",
            "Revoke less important decrees, restrict tariffs and trade policies to fewer goods, or increase authority through laws and technologies.",
        ),
    },
    {
        "schluessel": "einfluss",
        "stufe": "warnung",
        "warnung": False,
        "bedingung": """
            influence < 0
        """,
        "de": (
            "Einfluss im Minus",
            "Deine diplomatischen Verpflichtungen kosten mehr Einfluss, als du erzeugst. Das schwächt deine Diplomatie.",
            "Kündige unwichtige Pakte und gib Interessen in Regionen auf, die du nicht brauchst. Steigere den Einfluss über Gesetze, Technologien und einen höheren Rang.",
        ),
        "en": (
            "Negative Influence",
            "Your diplomatic commitments cost more influence than you produce. This weakens your diplomacy.",
            "Cancel unimportant pacts and drop interests in regions you do not need. Increase influence through laws, technologies and a higher rank.",
        ),
    },
    {
        "schluessel": "unruhe",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            any_scope_state = {
                is_incorporated = yes
                state_population >= 100000
                turmoil >= 0.25
            }
        """,
        "detail": {
            "scope": "berater_ort_unruhe",
            "typ": "state",
            "effekt": """
                ordered_scope_state = {
                    limit = {
                        is_incorporated = yes
                        state_population >= 100000
                    }
                    order_by = turmoil
                    max = 1
                    save_scope_as = berater_ort_unruhe
                }
            """,
            "de": "Am stärksten betroffen: {NAME}.",
            "en": "Most affected: {NAME}.",
        },
        "de": (
            "Unruhe in deinen Staaten",
            "In mindestens einem deiner Staaten herrscht starke Unruhe. Das senkt die Produktivität und kann zu Aufständen führen.",
            "Prüfe die betroffenen Staaten in der Bevölkerungsansicht: Arbeitslosigkeit, ein niedriger Lebensstandard und diskriminierte Kulturen sind die häufigsten Ursachen. Schaffe Arbeitsplätze und verbessere die Versorgung mit Grundgütern.",
        ),
        "en": (
            "Turmoil in Your States",
            "At least one of your states is in serious turmoil. This lowers productivity and can lead to uprisings.",
            "Inspect the affected states in the population view: unemployment, a low standard of living and discriminated cultures are the most common causes. Create jobs and improve the supply of basic goods.",
        ),
    },
    {
        "schluessel": "radikale",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            radical_fraction = {
                value >= 0.2
            }
        """,
        "de": (
            "Viele Radikale",
            "Mehr als 20 % deiner Bevölkerung sind radikal. Radikale stärken revolutionäre Bewegungen und schwächen die Regierung.",
            "Hebe den Lebensstandard (günstigere Grundgüter, höhere Löhne), senke die Steuerlast der Unterschicht und gehe auf die Forderungen unzufriedener Interessengruppen ein.",
        ),
        "en": (
            "Many Radicals",
            "More than 20 % of your population is radical. Radicals strengthen revolutionary movements and weaken the government.",
            "Raise the standard of living (cheaper basic goods, higher wages), lower the tax burden on the lower strata and address the demands of unhappy interest groups.",
        ),
    },
    {
        "schluessel": "ig_wuetend",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            any_interest_group = {
                is_powerful = yes
                ig_approval <= -10
            }
        """,
        "detail": {
            "scope": "berater_ig_wuetend",
            "typ": "ig",
            "effekt": """
                ordered_interest_group = {
                    limit = {
                        is_powerful = yes
                    }
                    order_by = berater_ig_unmut
                    max = 1
                    save_scope_as = berater_ig_wuetend
                }
            """,
            "de": "Am wütendsten ist {NAME}.",
            "en": "The angriest is {NAME}.",
        },
        "de": (
            "Mächtige Interessengruppe wütend",
            "Eine einflussreiche Interessengruppe ist wütend auf deine Regierung. Sie kann radikal werden und revolutionäre Bewegungen unterstützen.",
            "Prüfe in der Politikansicht, welche Gesetze die Gruppe ablehnt. Nimm sie in die Regierung auf, erfülle eine ihrer Forderungen oder schwäche sie gezielt durch Unterdrückung.",
        ),
        "en": (
            "Powerful Interest Group Angry",
            "An influential interest group is angry with your government. It may radicalize and back revolutionary movements.",
            "Check in the politics view which laws the group opposes. Bring it into the government, meet one of its demands or weaken it through suppression.",
        ),
    },
    {
        "schluessel": "arbeitslosigkeit",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            any_scope_state = {
                is_incorporated = yes
                state_population >= 250000
                state_unemployment_rate > 0.15
            }
        """,
        "detail": {
            "scope": "berater_ort_arbeitslos",
            "typ": "state",
            "effekt": """
                ordered_scope_state = {
                    limit = {
                        is_incorporated = yes
                        state_population >= 250000
                    }
                    order_by = berater_arbeitslose
                    max = 1
                    save_scope_as = berater_ort_arbeitslos
                }
            """,
            "de": "Die meisten Arbeitslosen gibt es in {NAME}. Der Bauplan bevorzugt solche Staaten.",
            "en": "The most unemployed live in {NAME}. The construction plan favors such states.",
        },
        "de": (
            "Hohe Arbeitslosigkeit",
            "In mindestens einem größeren Staat sind über 15 % der Arbeitskräfte ohne Arbeit. Arbeitslose verarmen und werden radikal.",
            "Baue dort Gebäude mit vielen Arbeitsplätzen (Landwirtschaft, Minen, Fabriken), für deren Güter es Nachfrage gibt. Gute Infrastruktur und Marktzugang helfen dabei.",
        ),
        "en": (
            "High Unemployment",
            "In at least one larger state more than 15 % of the workforce is unemployed. The unemployed grow poor and turn radical.",
            "Build buildings there that employ many workers (agriculture, mines, factories) and whose goods are in demand. Good infrastructure and market access help.",
        ),
    },
    {
        "schluessel": "lebensstandard",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            berater_anteil_unter_erwartung >= 0.3
        """,
        "de": (
            "Erwartungen enttäuscht",
            "Mehr als 30 % deiner Bevölkerung leben unter dem Lebensstandard, den sie erwarten. Das erzeugt Radikale.",
            "Senke die Preise für Grundgüter (Getreide, Stoffe, Holz, Möbel) durch mehr Produktion oder Importe, und stärke Löhne und Sozialgesetze.",
        ),
        "en": (
            "Expectations Unmet",
            "More than 30 % of your population lives below the standard of living they expect. This creates radicals.",
            "Lower the price of basic goods (grain, fabric, wood, furniture) through more production or imports, and strengthen wages and welfare laws.",
        ),
    },
    {
        "schluessel": "engpaesse",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            market = {
                market_number_goods_shortages >= 1
            }
        """,
        "de": (
            "Güterknappheit",
            "In deinem Markt fehlen Güter, die Betriebe als Vorprodukte brauchen. Das senkt ihre Produktivität und treibt die Preise.",
            "Der Bauplan im Journal nennt dir, was du wo bauen solltest. Alternativ helfen Importe über Handelsrouten.",
        ),
        "en": (
            "Goods Shortages",
            "Your market lacks goods that buildings need as inputs. This lowers their productivity and drives prices up.",
            "The construction plan in the journal tells you what to build where. Imports through trade routes also help.",
        ),
    },
    {
        "schluessel": "infamie_hoch",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            infamy >= infamy_threshold:notorious
            infamy < infamy_threshold:pariah
        """,
        "de": (
            "Hohe Infamie",
            "Deine Infamie hat die Stufe „berüchtigt“ erreicht. Weitere Eroberungen können Koalitionen gegen dich auslösen.",
            "Lege eine Pause bei aggressiven Kriegszielen ein und lass die Infamie sinken, bevor du die nächste Expansion beginnst.",
        ),
        "en": (
            "High Infamy",
            "Your infamy has reached the notorious level. Further conquests may trigger coalitions against you.",
            "Pause aggressive war goals and let your infamy decay before starting your next expansion.",
        ),
    },
    {
        "schluessel": "abspaltung",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            has_any_secessionists_growing = yes
        """,
        "de": (
            "Separatisten im Aufwind",
            "In deinem Land wächst eine Abspaltungsbewegung. Wird sie stark genug, bricht ein Sezessionskrieg aus.",
            "Verbessere die Lage der betroffenen Kultur: Gesetze zu Staatsbürgerschaft und Kultur lockern, den Lebensstandard heben und die Unruhe in den betroffenen Staaten senken.",
        ),
        "en": (
            "Secessionists Growing",
            "A secessionist movement is growing in your country. If it becomes strong enough, a war of secession will break out.",
            "Improve the situation of the affected culture: relax citizenship and culture laws, raise the standard of living and reduce turmoil in the affected states.",
        ),
    },
    {
        "schluessel": "legitimitaet",
        "stufe": "warnung",
        "warnung": True,
        "bedingung": """
            legitimacy < 25
        """,
        "de": (
            "Regierung kaum legitim",
            "Die Legitimität deiner Regierung ist sehr niedrig. Gesetze lassen sich schwerer verabschieden, und die Regierung verliert Rückhalt.",
            "Bilde die Regierung um: Nimm Interessengruppen auf, deren Ideologie zu deiner Staatsform passt, und setze auf wenige, starke Regierungsparteien.",
        ),
        "en": (
            "Government Barely Legitimate",
            "Your government's legitimacy is very low. Laws are harder to pass and the government is losing support.",
            "Reshuffle the government: include interest groups whose ideology fits your form of government, and rely on a few strong governing parties.",
        ),
    },
    # ------------------------------------------------------------------ tipp
    {
        "schluessel": "forschung",
        "stufe": "tipp",
        "warnung": False,
        "bedingung": """
            NOT = { is_researching_technology = any }
        """,
        "de": (
            "Keine Forschung aktiv",
            "Du erforschst gerade keine Technologie. Jede Woche ohne Forschungsziel verschwendet Innovation.",
            "Wähle in der Technologieansicht ein Ziel. Gute Prioritäten: Produktionstechnologien für deine wichtigsten Industrien, Eisenbahn sowie Verwaltungs- und Bildungstechnologien.",
        ),
        "en": (
            "No Active Research",
            "You are not researching any technology. Every week without a research goal wastes innovation.",
            "Pick a goal in the technology view. Good priorities: production technologies for your key industries, railways, and administration and education technologies.",
        ),
    },
    {
        "schluessel": "bau_leer",
        "stufe": "tipp",
        "warnung": False,
        "bedingung": """
            in_default = no
            scaled_debt < 0.6
            construction_queue_num_queued_government_levels < 1
        """,
        "de": (
            "Bauwirtschaft untätig",
            "Deine staatliche Bauwarteschlange ist leer. Die Baukapazität, die du bezahlst, bleibt ungenutzt.",
            "Plane neue Bauvorhaben: Betriebe für knappe oder teure Güter, Infrastruktur in Staaten mit Engpässen oder weitere Bausektoren, um künftig schneller zu bauen.",
        ),
        "en": (
            "Construction Idle",
            "Your government construction queue is empty. The construction capacity you pay for goes unused.",
            "Queue new projects: buildings for scarce or expensive goods, infrastructure in states with bottlenecks, or more construction sectors to build faster in the future.",
        ),
    },
    {
        "schluessel": "bau_lang",
        "stufe": "tipp",
        "warnung": True,
        "bedingung": """
            construction_queue_government_duration > 104
        """,
        "de": (
            "Bauwarteschlange zu lang",
            "Bis alle staatlichen Bauvorhaben fertig sind, vergehen mehr als zwei Jahre.",
            "Baue zusätzliche Bausektoren, sofern das Budget es zulässt, wechsle auf bessere Bau-Produktionsmethoden oder ordne die Warteschlange nach Wichtigkeit.",
        ),
        "en": (
            "Construction Queue Too Long",
            "It will take more than two years to finish all government construction projects.",
            "Build additional construction sectors if your budget allows, switch to better construction production methods, or reorder the queue by priority.",
        ),
    },
    {
        "schluessel": "gold_ungenutzt",
        "stufe": "tipp",
        "warnung": True,
        "bedingung": """
            is_at_war = no
            scaled_gold_reserves >= 0.9
        """,
        "de": (
            "Goldreserven fast voll",
            "Deine Goldreserven sind beinahe am Maximum. Überschüsse darüber hinaus verfallen ungenutzt.",
            "Investiere das Geld: mehr Bausektoren, Subventionen für wichtige Industrien, höhere Beamtengehälter oder niedrigere Steuern.",
        ),
        "en": (
            "Gold Reserves Nearly Full",
            "Your gold reserves are close to their maximum. Any surplus beyond that is wasted.",
            "Put the money to work: more construction sectors, subsidies for key industries, higher government wages or lower taxes.",
        ),
    },
    {
        "schluessel": "steuern_hoch",
        "stufe": "tipp",
        "warnung": True,
        "bedingung": """
            tax_level >= high
            scaled_debt < 0.1
            scaled_gold_reserves >= 0.5
        """,
        "de": (
            "Steuern senkbar",
            "Deine Steuern sind hoch, obwohl der Haushalt gut dasteht. Hohe Steuern drücken den Lebensstandard und das Wachstum.",
            "Senke die Steuerstufe um eine Stufe und beobachte die Wochenbilanz. Ein höherer Lebensstandard bringt mehr Loyalisten und Wachstum.",
        ),
        "en": (
            "Taxes Could Be Lowered",
            "Your taxes are high even though the budget is healthy. High taxes depress the standard of living and growth.",
            "Lower the tax level by one step and watch your weekly balance. A higher standard of living brings more loyalists and growth.",
        ),
    },
    {
        "schluessel": "alphabetisierung",
        "stufe": "tipp",
        "warnung": True,
        "bedingung": """
            literacy_rate < 0.25
            NOT = { has_law = law_type:law_public_schools }
        """,
        "de": (
            "Niedrige Alphabetisierung",
            "Weniger als ein Viertel deiner Bevölkerung kann lesen. Das bremst die Forschung und den Aufstieg in qualifizierte Berufe.",
            "Führe bessere Schulgesetze ein (z. B. öffentliche Schulen), investiere in die Institution Schulen und erforsche Bildungstechnologien.",
        ),
        "en": (
            "Low Literacy",
            "Less than a quarter of your population can read. This slows research and keeps pops out of qualified professions.",
            "Enact better school laws (e.g. public schools), invest in the schools institution and research education technologies.",
        ),
    },
    {
        "schluessel": "industriegueter_teuer",
        "stufe": "tipp",
        "warnung": True,
        "bedingung": """
            market = {
                OR = {
                    mg:coal = { market_goods_pricier >= 0.25 }
                    mg:iron = { market_goods_pricier >= 0.25 }
                    mg:wood = { market_goods_pricier >= 0.25 }
                    mg:tools = { market_goods_pricier >= 0.25 }
                    mg:steel = { market_goods_pricier >= 0.25 }
                }
            }
        """,
        "de": (
            "Industriegüter teuer",
            "Mindestens ein wichtiges Industriegut (Kohle, Eisen, Holz, Werkzeuge oder Stahl) kostet über 25 % mehr als der Grundpreis. Das bremst die ganze Industrie.",
            "Öffne im Journal den Bauplan: Der Berater nennt dir für jedes teure Gut das passende Gebäude und den besten Staat dafür.",
        ),
        "en": (
            "Industrial Goods Expensive",
            "At least one key industrial good (coal, iron, wood, tools or steel) costs more than 25 % above its base price. This holds back your whole industry.",
            "Open the construction plan in the journal: your advisor names the right building and the best state for each expensive good.",
        ),
    },
    {
        "schluessel": "gesetze",
        "stufe": "tipp",
        "warnung": False,
        "bedingung": """
            is_at_war = no
            enacting_any_law = no
        """,
        "de": (
            "Kein Gesetz in Arbeit",
            "Derzeit bringst du kein Gesetz auf den Weg. Reformen gehören zu den stärksten Hebeln für Wirtschaft und Stabilität.",
            "Öffne im Journal den Gesetzesplan: Der Berater empfiehlt dir konkrete Gesetze und sagt, ob deine Regierung sie mitträgt.",
        ),
        "en": (
            "No Law Being Enacted",
            "You are not enacting any law right now. Reforms are among the strongest levers for the economy and stability.",
            "Open the law plan in the journal: your advisor recommends specific laws and tells you whether your government backs them.",
        ),
    },
]
