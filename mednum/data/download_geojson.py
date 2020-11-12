from mednum.config import *
from mednum.tools import *
import logging

logging.basicConfig(level=logging.INFO)

def generer():
    if not geojson_path.exists():

        if not geojson_zip_file_path.exists():
            logging.info(
                "Download %s from %s " % (geojson_zip_file_path, url_france_geojson_zip)
            )

            download_file(url_france_geojson_zip, geojson_zip_file_path)

        unzip_file(geojson_zip_file_path, geojson_path)
