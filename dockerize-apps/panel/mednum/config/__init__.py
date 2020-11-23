
from pathlib import Path

hard_reset = False
data_path = Path("../data")

if not data_path.exists():
    data_path = Path("./data")

interim_data = data_path / "interim/"
processed_data = data_path / "processed/"
cache_dir = interim_data



map_idx_to_data_idx = {
    "Compétences usages numériques": "COMPÉTENCES NUMÉRIQUES / SCOLAIRES",
    "Compétences adminitratives": "COMPETENCES ADMINISTATIVES",
    "Accès à l'info": "ACCES A L'INFORMATION",
    "Accès aux interfaces numériques": "ACCÈS AUX INTERFACES NUMERIQUES",
    "Score": "SCORE GLOBAL ",
    "Population": "Population",
    "Taux de pauvreté": None,
    "Epuipement des ménages": None,
    "Couverture mobile": None,
    "Taux de couverture HD / THD": None,
}

selected_idx = ["Compétences usages numériques", "Accès à l'info"]
selected_data_idx = [
    dind for mind, dind in map_idx_to_data_idx.items() if mind in selected_idx
]

OPTIONS_INT_NUM = [
    "Accès aux interfaces numériques",
    "Taux de pauvreté",
    "Epuipement des ménages",
    "Couverture mobile",
    "Taux de couverture HD / THD",
]
OPTIONS_X_INFOS = ["Accès à l'info", "Oui", "Non"]
OPTIONS_X_COMP_ADMIN = ["Compétences adminitratives", "Oui", "Non"]
OPTIONS_X_COMP_USAGE = ["Compétences usages numériques", "Oui", "Non"]

CATEGORIES_INT_NUM = {
    "select_all": "Accès aux interfaces numériques",
    "select_options": OPTIONS_INT_NUM,
}
INDICE = "GLOBAL COMPETENCES"


OPTIONS_INT_NUM = [
        "Taux de pauvreté",
        "Equipement des ménages",
        "Couverture mobile",
        "Taux de couverture HD / THD",
    ]
CATEGORIES_INT_NUM = {
    "select_all": "Accès aux interfaces numériques",
    "select_options": OPTIONS_INT_NUM,
}

OPTIONS_X_INFOS = ["Oui", "Non"]
CATEGORIES_X_INFOS = {
    "select_all": "Accès à l'info",
    "select_options": OPTIONS_X_INFOS,
}

OPTIONS_X_COMP_ADMIN = ["Oui", "Non"]
CATEGORIES_X_COMP_ADMIN = {
    "select_all": "Compétences adminitratives",
    "select_options": OPTIONS_X_COMP_ADMIN,
}

OPTIONS_X_COMP_USAGE = ["Oui", "Non"]
CATEGORIES_X_COMP_USAGE = {
    "select_all": "Compétences usages numériques",
    "select_options": OPTIONS_X_COMP_USAGE,
}

TREEVIEW_CHECK_BOX = {
                "interfaces_num":CATEGORIES_INT_NUM,
            "infos_num": CATEGORIES_X_INFOS,
            "comp_admin": CATEGORIES_X_COMP_ADMIN,
            "comp_usage_num": CATEGORIES_X_COMP_USAGE,
}
