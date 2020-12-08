from pathlib import Path

hard_reset = False
data_path = Path("../data")

if not data_path.exists():
    data_path = Path("./data")

interim_data = data_path / "interim/"
processed_data = data_path / "processed/"
cache_dir = interim_data

INDICE = "GLOBAL COMPETENCES"

MAP_COL_WIDGETS = {
    "level_0": {"index": "insee_com", "names": "nom_com"},
    "level_1": {
        # "Pays": "",
        "Région": "insee_reg",
        "Département": "insee_dep",
        "Intercommune": "EPCI",
        "Commune": "insee_com",
        "Iris": "code_iris",
    },
}
SELECT = list(MAP_COL_WIDGETS["level_1"].keys())

CATEGORIES_INT_NUM = {
    "TX_POVERTY": {
        "nom": "Taux de pauvreté",
        "desc": """Proportion des ménages dont les revenus sont inférieurs à 60% du revenu médian""",
        "aggfunc": "median",
    },
    "COUVERTURE_MOBILE": {
        "nom": "Couverture mobile",
        "desc": """Proportion du territoire d'où l'on peut accéder à un réseau de téléphonie mobile""",
        "aggfunc": "mean",
    },
    "TAUX_COUVERTURE_THD": {
        "nom": "Taux de couverture HD / THD",
        "desc": """Proportion des bâtiments reliés à internet Haut Débit ou Très Haut Débit""",
        "aggfunc": "mean",
    },
    "nom": "Accès interfaces numériques",
    "desc": "Identification des territoires mal couverts par les réseaux ou dans lesquels des populations auront des difficultésfinancières à y accéder ou à s'équiper en terminaux numériques",
}


def reverse_key_val(d):
    d_rev = {}
    for opt, val in d.items():
        if opt not in ["nom", "desc"]:
            d_rev[val["nom"]] = opt
    return d_rev


CATEGORIES_X_INFOS = {
    "nom": "Accès information",
    "desc": "Identification des populations parmi lesquelles s’observent des difficultés à accomplir des démarches administratives",
    "TX_MENSEUL": {
        "nom": "Part des ménages d'une personne",
        "desc": """Proportion des personnes qui vivent seules parmi l'ensemble des ménages""",
        "aggfunc": "median",
    },
    "TX_FAMMONO": {
        "nom": "Part des ménages monoparentaux",
        "desc": "Proportion des personnes vivant seules avec enfants parmi l'ensemble des ménages",
        "aggfunc": "median",
    },
    "ACCES_SERVICE_PUBLIC": {
        "nom": "Accès à un point physique de service public",
        "desc": "Nombre de lieux d'accueil et d'information de services publics ou parapublics pour 1000 habitants (liste des mediathèques)",
        "aggfunc": "mean",
    },
}


CATEGORIES_X_COMP_ADMIN = {
    "TX_25ETMOINS": {
        "nom": "Part des moins de 25 ans",
        "desc": """Proportion de jeunes de moins de 25 ans dans la population du territoire""",
        "aggfunc": "median",
    },
    "TX_RSA": {
        "nom": "Part des bénéficiaires de minimas sociaux",
        "desc": "Proportion des personnes qui percoivent des aides sociales (RSA, AAH, ASPA,...) parmi la population du territoire",
        "aggfunc": "median",
    },
    "TX_DEMANDEUR_EMPLOIS": {
        "nom": "Part des chômeurs (15-64 ans)",
        "desc": "Proportion de personnes en recherche d'emploi et n'ayant pas travaillé récemment parmi la population en âge de travailler du territoire",
        "aggfunc": "median",
    },
    "nom": "Compétences adminitratives",
    "desc": "Identification des populations parmi lesquelles s’observent des difficultés à accomplir des démarches administratives",
}


CATEGORIES_X_COMP_USAGE = {
    "nom": "Compétences usages numériques",
    "desc": "Identification des populations parmi lesquelles s’observe une fréquence d’illectronisme ou difficulté à utiliser internet",
    "TX_65ETPLUS": {
        "nom": "Part des personnes âgés de plus de 65 ans",
        "desc": """Proportion des personnes âgées de plus de 65 ans dans la population du territoire""",
        "aggfunc": "median",
    },
    "TX_NSCOL15P": {
        "nom": "Part des personnes pas/peu diplômés de 15 ans et plus",
        "desc": "Proportion des personnes sans diplôme ou avec des diplôme de niveau inférieur au baccalauréat parmi la population du territoire âgée de plus de 15 ans",
        "aggfunc": "median",
    },
}

TOUT = {
    "nom": "Tous",
    "desc": "Sélections de l'ensemble des indicateurs",
}


CATEGORIES_INT_NUM_REV = reverse_key_val(CATEGORIES_INT_NUM)
CATEGORIES_X_INFOS_REV = reverse_key_val(CATEGORIES_X_INFOS)
CATEGORIES_X_COMP_ADMIN_REV = reverse_key_val(CATEGORIES_X_COMP_ADMIN)
CATEGORIES_X_COMP_USAGE_REV = reverse_key_val(CATEGORIES_X_COMP_USAGE)
CATEGORIES_INDICES_REV = {
    **CATEGORIES_INT_NUM_REV,
    **CATEGORIES_X_INFOS_REV,
    **CATEGORIES_X_COMP_ADMIN_REV,
    **CATEGORIES_X_COMP_USAGE_REV,
}

CATEGORIES_INDICES = {v: k for k, v in CATEGORIES_INDICES_REV.items()}

AXES_INDICES = {
    "interfaces_num": CATEGORIES_INT_NUM,
    "infos_num": CATEGORIES_X_INFOS,
    "comp_admin": CATEGORIES_X_COMP_ADMIN,
    "comp_usage_num": CATEGORIES_X_COMP_USAGE,
}
# TREEVIEW_CHECK_BOX = {"tout_axes": TOUT, **AXES_INDICES}
TREEVIEW_CHECK_BOX = {**AXES_INDICES}

