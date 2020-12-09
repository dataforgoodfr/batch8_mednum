from pathlib import Path

data_path = Path('./data')
if not data_path.exists():
    data_path = Path('../data')

external_data = data_path / 'external/'
processed_data = data_path / 'processed/'
raw_data = data_path / 'raw/'
interim_data = data_path / 'interim/'

# France Geojson
url_france_geojson_zip = 'https://github.com/gregoiredavid/france-geojson/archive/master.zip'
geojson_path = external_data / "france-geojson"
geojson_zip_file_path = geojson_path.with_suffix(".zip")

# Data gouv
url_data_gouv_geojson_zip = "https://public.opendatasoft.com/explore/dataset/contours-iris/download/?format=geojson&timezone=Europe/Berlin&lang=fr"
data_gouv_geojson_file_path = external_data / "france-geojson"/ "contours-iris.geojson"

# Base Couples-Familles-Ménages en 2017 INSEE
url_cc_coupl_fam_men_2017_COM = "https://www.insee.fr/fr/statistiques/fichier/4515503/base-ccc-coupl-fam-men-2017-COM.zip"
base_cc_coupl_fam_men_2017_COM_path = external_data / "base-cc-coupl-fam-men-2017-COM"
base_cc_coupl_fam_men_2017_COM_zip = base_cc_coupl_fam_men_2017_COM_path.with_suffix(".zip")

# Populations légales 2017 INSEE (région, département, commune, arrondissement)
url_insee_recensement_2017_zip = "https://www.insee.fr/fr/statistiques/fichier/4265429/ensemble.zip"
insee_recensement_path = external_data / "ensemble"/ "Communes.csv"
insee_recensement_zip_path = external_data / "ensemble.zip"

# Bénéficiaires des minimas sociaux (RSA socle)
url_insee_minimas_sociaux = "https://www.insee.fr/fr/statistiques/fichier/2500444/beneficiaires_CAF_31-12-2015.xls"
insee_minimas_sociaux_path = external_data / "beneficiaires_CAF_31-12-2015.xls"
