import gzip
import json
import os.path
import shutil
from datetime import datetime, timedelta
from enum import Enum


class ContentType(Enum):
    MOVIE = 1
    SERIES = 2


def generate_id_exports_url(content_type):
    # Daily id exports starts at 7-8 UTC, so to be sure we subtract 10 hours
    current_date = (datetime.utcnow() - timedelta(hours=10)).date().strftime("%m_%d_%Y")
    if content_type == ContentType.MOVIE:
        base_url = "https://files.tmdb.org/p/exports/movie_ids_"
    elif content_type == ContentType.SERIES:
        base_url = "https://files.tmdb.org/p/exports/tv_series_ids_"
    else:
        raise ValueError(f"Invalid content_type. Can only use ContentType.MOVIE or ContentType.SERIES. "
                         f"Got {content_type}")
    url = f"{base_url}{current_date}.json.gz"
    return url


def get_data_filename(content_type):
    return f"{content_type}_data.json"


def save_id_data(download_path, filename, content):
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    with open(os.path.join(download_path, filename), "wb") as file:
        file.write(content)


def extract_gz(download_path, original_filename, extracted_filename):
    with gzip.open(os.path.join(download_path, original_filename), "rb") as f_in:
        with open(os.path.join(download_path, extracted_filename), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_data_ids(filepath):
    with open(filepath, "rb") as file:
        for line in file:
            json_data = json.loads(line)
            item_id = json_data.get("id")
            if item_id:
                yield item_id
