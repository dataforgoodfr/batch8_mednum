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
url_data_gouv_geojson_zip = "https://www.data.gouv.fr/fr/datasets/r/3665b916-1a0b-4cbe-9bde-eabfcab29872"
data_gouv_geojson_file_path = external_data / "france-geojson"/ "contours-iris.geojson"
