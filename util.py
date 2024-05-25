import pandas as pd

def write_to_csv(rows, out_file):
    pd.DataFrame(rows).to_csv(out_file, index=False)