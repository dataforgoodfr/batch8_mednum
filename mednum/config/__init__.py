from pathlib import Path

external_data = Path('./data/external/')
processed_data = Path('./data/processed/')
raw_data = Path('./data/raw/')
interim_data = Path('./data/interim/')

# France Geojson
url_france_geojson_zip = 'https://github.com/gregoiredavid/france-geojson/archive/master.zip'
geojson_path = external_data / "france-geojson"
geojson_zip_file_path = geojson_path.with_suffix(".zip")

# Data gouv
url_data_gouv_geojson_zip = "https://www.data.gouv.fr/fr/datasets/r/3665b916-1a0b-4cbe-9bde-eabfcab29872"
data_gouv_geojson_file_path = external_data / "france-geojson"/ "contours-iris.geojson"
