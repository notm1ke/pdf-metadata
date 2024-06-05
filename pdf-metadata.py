import os
import json
import argparse
import exiftool
import requests
import pandas as pd

from time import sleep, time
from util import validate_url, with_backoff, write_to_csv

parser = argparse.ArgumentParser(
    prog="pdf-metadata",
    description='Download PDFs from a source CSV file and extracts their metadata.'
)

parser.add_argument('-i', '--input', help='path to the source csv file', required=True)
parser.add_argument('-m', '--mode', help='mode to run the script in', choices=['json', 'csv'], default='csv')

args = parser.parse_args()
source_csv = args.input
source_name = source_csv.split('/')[-1].split('.csv')[0]

if not os.path.exists(source_csv):
    print(f'ERROR: File `{source_csv}` does not exist.')
    exit(1)

if not source_csv.endswith('.csv'):
    print(f'ERROR: File `{source_csv}` is not a CSV file.')
    exit(1)

start = time()
pd = pd.read_csv(source_csv)

if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

if not os.path.exists('pdfs/meta'):
    os.makedirs('pdfs/meta')

files = {}
clean_pd = pd.dropna(subset=['Url'])

for i, row in clean_pd.iterrows():
    # skip if not a pdf by mime type
    mime = row.get('Mime type', None)
    if mime != 'application/pdf':
        print(f'[{i + 1}] Target is not a PDF file (expected: application/pdf, found: {mime if mime is not None else "<unknown>"})')
        continue

    # get url, or skip if empty
    url = row.get('Url', None)
    if url is None:
        print(f'[{i + 1}] Skipping empty URL..')
        continue

    # check if url is valid
    valid_url = validate_url(str(url))
    if not valid_url:
        print(f'[{i + 1}] Skipping invalid URL: {url}')
        continue

    # check if file was deleted
    deleted_at = str(row.get('Deleted at', float('nan')))
    if deleted_at is not None and deleted_at != 'nan':
        print(f'[{i + 1}] Skipping {url} as it has been deleted.. ({deleted_at})')
        continue

    filename = f'pdfs/{source_name}-{url.split("/")[-1]}'
    if not url.endswith('.pdf'):
        print(f'[{i + 1}] Skipping {url} as it is not a PDF file..')
        continue

    # save the url to the resolver
    files[filename.split('pdfs/')[1]] = url

    # check if the file already exists, skip if so
    if os.path.exists(filename):
        print(f'[{i + 1}] {filename} already downloaded, skipping..')
        continue

    # download the file and sleep for 0.25 seconds
    with open(filename, 'wb') as f:
        response = with_backoff(lambda: requests.get(url, timeout=5))
        content = response.content
        f.write(content)
        sleep(0.5)

    print(f'[{i + 1}] Downloaded to {filename}')

i = 0
mode = args.mode
rows = []

for pdf in os.listdir('pdfs'):
    i += 1

    # skip non-pdf files
    if not pdf.endswith('.pdf'):
        continue

    # skip already processed files
    filename = f'pdfs/{pdf}'
    if os.path.exists(f'pdfs/meta/{pdf}.json') and mode == 'json':
        print(f'[{i}] Metadata for {filename} already exists, skipping..')
        continue

    # extract metadata and save it to a json file
    try:
        with exiftool.ExifToolHelper() as exif:
            meta = exif.get_metadata(filename)[0]
            payload = {
                'url': files.get(pdf, '<unknown url>'),
                'title': meta.get('PDF:Title', '<unknown title>'),
                'author': meta.get('PDF:Author', '<unknown author>'),
                'creator': meta.get('PDF:Creator', '<unknown creator>'),
                'producer': meta.get('PDF:Producer', '<unknown producer>'),
                'version': meta.get('PDF:PDFVersion', '<unknown version>'),
                'size': meta.get('File:FileSize', -1),
                'xmp': meta.get('XMP:XMPToolkit', '<unknown xmp toolkit version>'),
                'pages': meta.get('PDF:PageCount', -1)
            }

            if mode == 'json':
                with open(f'pdfs/meta/{source_name}-{pdf}.json', 'w') as out:
                    out.write(json.dumps(payload, indent=3))
            else: rows.append(payload)

            print(f'[{i}] {"Saved" if mode == "json" else "Collected"} metadata for {filename}')
    except Exception as e:
        print(f'[{i}] Error processing {filename}: {e}')

if mode == 'csv' and len(rows) > 0:
    write_to_csv(rows, f'{source_name}-metadata.csv')
    print(f'Wrote metadata for {len(rows)} PDFs to {source_name}-metadata.csv')

print(f'Processed {i} PDFs in {time() - start:.2f} seconds.')