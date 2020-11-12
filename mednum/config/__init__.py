from pathlib import Path
from tqdm import tqdm

external_data = Path('./data/external/')
processed_data = Path('./data/processed/')
raw_data = Path('./data/raw/')
interim_data = Path('./data/interim/')

# France Geojson
url_france_geojson_zip = 'https://github.com/gregoiredavid/france-geojson/archive/master.zip'
geojson_path = external_data / "france-geojson"
geojson_zip_file_path = geojson_path.with_suffix(".zip")
