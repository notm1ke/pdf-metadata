import pandas as pd

from time import sleep
from urllib.parse import urlparse

def write_to_csv(rows, out_file):
    pd.DataFrame(rows).to_csv(out_file, index=False)

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

def with_backoff(func, max_retries=3, factor=2):
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            print(f'Error: {e}')
            sleep(factor ** retries)
            retries += 1

    raise Exception(f'Failed after {retries} retries..' if retries == retries else 'Failed..')