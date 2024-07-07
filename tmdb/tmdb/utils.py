import gzip
import json
import os.path
import shutil
from datetime import datetime, timedelta


def generate_id_exports_url():
    # Daily id exports starts at 7-8 UTC, so to be sure we subtract 10 hours
    current_date = (datetime.utcnow() - timedelta(hours=10)).date().strftime("%m_%d_%Y")
    url = f"https://files.tmdb.org/p/exports/movie_ids_{current_date}.json.gz"
    return url


def save_id_data(download_path, filename, content):
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    with open(os.path.join(download_path, filename), "wb") as file:
        file.write(content)


def extract_gz(download_path, original_filename, extracted_filename):
    with gzip.open(os.path.join(download_path, original_filename), "rb") as f_in:
        with open(os.path.join(download_path, extracted_filename), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_movie_ids(filepath):
    with open(filepath, "rb") as file:
        for line in file:
            json_data = json.loads(line)
            movie_id = json_data.get("id")
            if movie_id:
                yield movie_id
