

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
