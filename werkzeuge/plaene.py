"""Daten für Bauplan (berater.3) und Gesetzesplan (berater.4).

GUETER: Güter, die der Bauplan beobachtet, in Reihenfolge der Wichtigkeit.
    Ist ein Gut im Markt teurer als PREIS_SCHWELLE über dem Grundpreis, sucht der
    Berater den besten eigenen Staat, in dem eines der Gebäude gebaut werden kann
    (erstes baubares Gebäude der Liste gewinnt). Höchstens MAX_GUETER Güter je Plan.

GESETZE: Gesetzesempfehlungen in Reihenfolge der Wichtigkeit. Eine Empfehlung gilt,
    wenn das Land eines der Gesetze in "von" hat, eines der Gesetze in "nach"
    verabschiedet werden kann und "bedingung" (Länder-Scope) erfüllt ist.
    Höchstens MAX_GESETZE Empfehlungen je Plan.

Alle Schlüssel sind gegen die Lokalisierung des Grundspiels geprüft.
"""

PREIS_SCHWELLE = 0.2
MAX_GUETER = 5
MAX_GESETZE = 4

# (Schlüssel, Deutsch, Englisch, Gebäude)
GUETER = [
    ("coal", "Kohle", "Coal", ["building_coal_mine"]),
    ("iron", "Eisen", "Iron", ["building_iron_mine"]),
    ("wood", "Holz", "Wood", ["building_logging_camp"]),
    ("tools", "Werkzeuge", "Tools", ["building_tooling_workshop"]),
    ("steel", "Stahl", "Steel", ["building_steel_mill"]),
    ("fabric", "Stoffe", "Fabric", ["building_cotton_plantation"]),
    ("glass", "Glas", "Glass", ["building_glassworks"]),
    ("paper", "Papier", "Paper", ["building_paper_mill"]),
    ("sulfur", "Schwefel", "Sulfur", ["building_sulfur_mine"]),
    ("lead", "Blei", "Lead", ["building_lead_mine"]),
    ("explosives", "Sprengstoff", "Explosives", ["building_explosives_factory"]),
    ("fertilizer", "Dünger", "Fertilizer", ["building_chemical_plant"]),
    ("engines", "Motoren", "Engines", ["building_motor_industry"]),
    ("oil", "Öl", "Oil", ["building_oil_rig"]),
    ("rubber", "Kautschuk", "Rubber", ["building_rubber_plantation"]),
    ("hardwood", "Edelholz", "Hardwood", ["building_logging_camp", "building_tropical_wood_lodge"]),
    ("dye", "Farbstoffe", "Dye", ["building_dye_plantation"]),
    ("electricity", "Elektrizität", "Electricity", ["building_power_plant"]),
    ("transportation", "Transportleistung", "Transportation", ["building_railway"]),
    ("grain", "Getreide", "Grain", [
        "building_wheat_farm", "building_rye_farm", "building_rice_farm",
        "building_maize_farm", "building_millet_farm",
    ]),
    ("groceries", "Lebensmittel", "Groceries", ["building_food_industry"]),
    ("clothes", "Kleidung", "Clothes", ["building_textile_mill"]),
    ("furniture", "Möbel", "Furniture", ["building_furniture_manufactory"]),
    ("meat", "Fleisch", "Meat", ["building_livestock_ranch"]),
    ("fish", "Fisch", "Fish", ["building_fishing_wharf"]),
    ("fruit", "Obst", "Fruit", ["building_orchard", "building_banana_plantation"]),
    ("sugar", "Zucker", "Sugar", ["building_sugar_plantation"]),
    ("liquor", "Spirituosen", "Liquor", ["building_food_industry"]),
    ("wine", "Wein", "Wine", ["building_vineyard"]),
    ("tobacco", "Tabak", "Tobacco", ["building_tobacco_plantation"]),
    ("coffee", "Kaffee", "Coffee", ["building_coffee_plantation"]),
    ("tea", "Tee", "Tea", ["building_tea_plantation"]),
    ("services", "Dienstleistungen", "Services", ["building_urban_center"]),
    ("porcelain", "Porzellan", "Porcelain", ["building_glassworks"]),
    ("luxury_clothes", "Luxuskleidung", "Luxury Clothes", ["building_textile_mill"]),
    ("luxury_furniture", "Luxusmöbel", "Luxury Furniture", ["building_furniture_manufactory"]),
    ("silk", "Seide", "Silk", ["building_silk_plantation"]),
    ("small_arms", "Handfeuerwaffen", "Small Arms", ["building_arms_industry"]),
    ("ammunition", "Munition", "Ammunition", ["building_munition_plant"]),
    ("artillery", "Artillerie", "Artillery", ["building_artillery_foundry"]),
    ("telephones", "Telefone", "Telephones", ["building_electrics_industry"]),
    ("radios", "Radios", "Radios", ["building_electrics_industry"]),
    ("automobiles", "Automobile", "Automobiles", ["building_automotive_industry"]),
]

GESETZE = [
    {
        "schluessel": "leibeigenschaft",
        "von": ["law_serfdom"],
        "nach": ["law_tenant_farmers", "law_commercialized_agriculture"],
        "bedingung": "",
        "de": "Leibeigene sind an das Land gebunden und fehlen deiner Industrie. Freie Bauern können in Minen und Fabriken arbeiten.",
        "en": "Serfs are tied to the land and unavailable to your industry. Free peasants can take jobs in mines and factories.",
    },
    {
        "schluessel": "wirtschaft",
        "von": ["law_traditionalism", "law_agrarianism"],
        "nach": ["law_interventionism", "law_laissez_faire"],
        "bedingung": "",
        "de": "Erst eine moderne Wirtschaftsordnung lässt private Investitionen und Industrie richtig wachsen.",
        "en": "Only a modern economic system lets private investment and industry grow properly.",
    },
    {
        "schluessel": "beamte",
        "von": ["law_hereditary_bureaucrats"],
        "nach": ["law_appointed_bureaucrats"],
        "bedingung": "",
        "de": "Erbliche Beamte sind teuer und ineffizient. Ernannte Beamte erzeugen mehr Bürokratie.",
        "en": "Hereditary bureaucrats are expensive and inefficient. Appointed bureaucrats produce more bureaucracy.",
    },
    {
        "schluessel": "handel",
        "von": ["law_isolationism"],
        "nach": ["law_mercantilism", "law_protectionism"],
        "bedingung": "",
        "de": "Isolationismus schneidet dich vom Welthandel ab. Importe würden Engpässe beheben und Preise senken.",
        "en": "Isolationism cuts you off from world trade. Imports would fix shortages and lower prices.",
    },
    {
        "schluessel": "schulen",
        "von": ["law_no_schools"],
        "nach": ["law_religious_schools", "law_private_schools", "law_public_schools"],
        "bedingung": "",
        "de": "Ohne Schulen bleibt die Bevölkerung ungebildet. Das bremst die Forschung und den Aufstieg in qualifizierte Berufe.",
        "en": "Without schools your population stays uneducated, which slows research and keeps pops out of qualified jobs.",
    },
    {
        "schluessel": "landsteuer",
        "von": ["law_land_based_taxation"],
        "nach": ["law_per_capita_based_taxation", "law_proportional_taxation"],
        "bedingung": "",
        "de": "Die Landsteuer belastet fast nur die Bauern. Eine breitere Steuerbasis bringt deutlich mehr Einnahmen.",
        "en": "Land-based taxation falls almost entirely on peasants. A broader tax base brings in much more revenue.",
    },
    {
        "schluessel": "verbrauchsteuer",
        "von": ["law_consumption_based_taxation"],
        "nach": ["law_per_capita_based_taxation", "law_proportional_taxation"],
        "bedingung": """
            OR = {
                berater_problem_defizit = yes
                berater_problem_schulden_hoch = yes
                berater_problem_schulden_kritisch = yes
            }
        """,
        "de": "Dein Haushalt braucht mehr Geld. Direkte Steuern bringen mehr ein als reine Verbrauchsteuern.",
        "en": "Your budget needs more money. Direct taxes raise more than consumption taxes alone.",
    },
    {
        "schluessel": "staatsbuergerschaft",
        "von": ["law_ethnostate", "law_national_supremacy"],
        "nach": ["law_racial_segregation", "law_cultural_exclusion"],
        "bedingung": """
            OR = {
                berater_problem_abspaltung = yes
                berater_problem_unruhe = yes
                berater_problem_radikale = yes
            }
        """,
        "de": "Diskriminierte Kulturen sind eine Hauptquelle deiner Unruhe und Separatisten. Mehr Rechte für Minderheiten nehmen den Druck heraus.",
        "en": "Discriminated cultures are a main source of your unrest and secessionists. More rights for minorities relieve the pressure.",
    },
    {
        "schluessel": "polizei",
        "von": ["law_no_police"],
        "nach": ["law_local_police"],
        "bedingung": """
            OR = {
                berater_problem_unruhe = yes
                berater_problem_radikale = yes
            }
        """,
        "de": "Ohne Polizei kann der Staat Unruhe kaum eindämmen.",
        "en": "Without police the state can hardly contain unrest.",
    },
    {
        "schluessel": "arbeiterrechte",
        "von": ["law_no_workers_rights"],
        "nach": ["law_regulatory_bodies"],
        "bedingung": """
            OR = {
                berater_problem_radikale = yes
                berater_problem_lebensstandard = yes
            }
        """,
        "de": "Aufsichtsbehörden verbessern die Arbeitsbedingungen und senken so die Zahl der Radikalen.",
        "en": "Regulatory bodies improve working conditions and thereby reduce radicals.",
    },
    {
        "schluessel": "sozialhilfe",
        "von": ["law_no_social_security"],
        "nach": ["law_poor_laws"],
        "bedingung": """
            berater_problem_lebensstandard = yes
            scaled_debt < 0.3
        """,
        "de": "Armengesetze fangen die Ärmsten auf und heben den Lebensstandard am unteren Ende.",
        "en": "Poor laws support the poorest and lift the standard of living at the bottom.",
    },
    {
        "schluessel": "oeffentliche_schulen",
        "von": ["law_religious_schools", "law_private_schools"],
        "nach": ["law_public_schools"],
        "bedingung": """
            literacy_rate < 0.6
            scaled_debt < 0.3
        """,
        "de": "Öffentliche Schulen heben die Alphabetisierung am schnellsten. Dein Haushalt kann sich das leisten.",
        "en": "Public schools raise literacy fastest, and your budget can afford them.",
    },
    {
        "schluessel": "kinderarbeit",
        "von": ["law_child_labor_allowed"],
        "nach": ["law_restricted_child_labor"],
        "bedingung": """
            literacy_rate < 0.5
        """,
        "de": "Kinder in die Schule statt in die Fabrik: Das steigert die Alphabetisierung und langfristig die Qualifikation.",
        "en": "Children in school instead of factories raises literacy and, in the long run, qualifications.",
    },
    {
        "schluessel": "gesundheit",
        "von": ["law_no_health_system"],
        "nach": ["law_charitable_health_system"],
        "bedingung": "",
        "de": "Armenhospitäler senken die Sterblichkeit und lassen die Bevölkerung schneller wachsen.",
        "en": "Charity hospitals lower mortality and let your population grow faster.",
    },
    {
        "schluessel": "armee",
        "von": ["law_peasant_levies"],
        "nach": ["law_professional_army"],
        "bedingung": "",
        "de": "Bauernaufgebote ziehen im Krieg Arbeitskräfte aus der Wirtschaft ab. Eine Berufsarmee ist schlagkräftiger.",
        "en": "Peasant levies drain workers from the economy in wartime. A professional army fights better.",
    },
    {
        "schluessel": "vielvoelker",
        "von": ["law_racial_segregation", "law_cultural_exclusion"],
        "nach": ["law_multicultural"],
        "bedingung": """
            berater_problem_abspaltung = yes
        """,
        "de": "Separatisten gewinnen an Boden. Volle Bürgerrechte für alle Kulturen nehmen ihnen den Grund zum Aufstand.",
        "en": "Secessionists are gaining ground. Full citizenship for all cultures removes their reason to revolt.",
    },
]
