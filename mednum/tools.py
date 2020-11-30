import requests
import logging
import zipfile
from tqdm.auto import tqdm
import logging


def download_file(url, filepath):
    with open(filepath, "wb") as f:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        for data in response.iter_content(block_size):
            if data:  # filter out keep-alive new chunks
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            logging.error("Download fails")

def unzip_file(zippath, output_path):
    with zipfile.ZipFile(zippath, "r") as zip_ref:
        logging.info("Extracting to %s " % output_path)
        zip_ref.extractall(output_path)