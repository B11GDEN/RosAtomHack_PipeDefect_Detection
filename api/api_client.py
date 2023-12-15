import requests

from pathlib import Path
from os import listdir
from os.path import isfile, join


def main():
    url_base = 'http://localhost:8000/'
    url_processing = url_base + 'processing'

    img_dir = Path(__file__).absolute().parents[1] / 'imgs'

    if check_connection(url=url_base) != 200:
        return

    files = prepare_files(img_dir=img_dir)

    resp = requests.post(url=url_processing, files=files)
    print(resp.json())


def check_connection(url: str):
    return requests.get(url).status_code


def prepare_files(img_dir: Path | str):
    file_names = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
    files = []
    for filename in file_names:
        files.append(('files', open(img_dir / filename, 'rb')))
    return files


if __name__ == '__main__':
    main()
