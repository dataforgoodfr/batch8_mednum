from mednum.config import *
from mednum.tools import *
import logging
import shutil

logging.basicConfig(level=logging.INFO)

def generer():
    if not base_cc_coupl_fam_men_2017_COM_path.exists():
        if not base_cc_coupl_fam_men_2017_COM_zip.exists():
            logging.info(
                "Download %s from %s " % (base_cc_coupl_fam_men_2017_COM_path, url_data_gouv_geojson_zip)
            )

            download_file(url_data_gouv_geojson_zip, base_cc_coupl_fam_men_2017_COM_zip)

        unzip_file(base_cc_coupl_fam_men_2017_COM_zip, base_cc_coupl_fam_men_2017_COM_path)

        