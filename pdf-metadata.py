import os
import json
import argparse
import exiftool
import requests
import pandas as pd

from time import sleep, time
from util import write_to_csv

parser = argparse.ArgumentParser(
    prog="pdf-metadata",
    description='Download PDFs from a source CSV file and extracts their metadata.'
)

parser.add_argument('-i', '--input', help='path to the source csv file', required=True)
parser.add_argument('-c', '--clean', help='clean the csv file before processing', action='store_true')
parser.add_argument('-m', '--mode', help='mode to run the script in', choices=['json', 'csv'], default='csv')

args = parser.parse_args()
source_csv = args.input
if not os.path.exists(source_csv):
    print(f'ERROR: File `{source_csv}` does not exist.')
    exit(1)

if not source_csv.endswith('.csv'):
    print(f'ERROR: File `{source_csv}` is not a CSV file.')
    exit(1)

if args.clean:
    pd = pd.read_csv(source_csv)
    pd = pd.dropna(subset=['Url'])
    pd.to_csv('clean.csv', index=False)
    source_csv = 'clean.csv'

start = time()
pd = pd.read_csv(source_csv)

if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

if not os.path.exists('pdfs/meta'):
    os.makedirs('pdfs/meta')

files = {}
for i, row in pd.iterrows():
    url = row['Url']
    filename = f'pdfs/{url.split("/")[-1]}'
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
        f.write(requests.get(url, timeout=2).content)
        sleep(0.25)

    print(f'[{i + 1}] Downloaded {url} to {filename}')

i = 0
mode = args.mode
rows = []

for pdf in os.listdir('pdfs'):
    i += 1

    # skip non-pdf files
    if not pdf.endswith('.pdf'):
        print(f'[{i}] Skipping {pdf} as it is not a PDF file')
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
                with open(f'pdfs/meta/{pdf}.json', 'w') as out:
                    out.write(json.dumps(payload, indent=3))
            else: rows.append(payload)

            print(f'[{i}] {"Saved" if mode == "json" else "Collected"} metadata for {filename}')
    except Exception as e:
        print(f'[{i}] Error processing {filename}: {e}')

if mode == 'csv' and len(rows) > 0:
    write_to_csv(rows, 'metadata.csv')
    print(f'Wrote metadata for {len(rows)} PDFs to metadata.csv')

print(f'Processed {i} PDFs in {time() - start:.2f} seconds.')