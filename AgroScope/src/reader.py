import pandas as pd 
def read_csv(file_input) -> pd.DataFrame:
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
    for enc in encodings:
        try:
            if isinstance(file_input, str):
                return pd.read_csv(file_input, sep=';', decimal=',', quotechar='"', encoding=enc)
            elif hasattr(file_input, 'read'):
                file_input.seek(0)
                return pd.read_csv(file_input, sep=';', decimal=',', quotechar='"', encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode file with tried encodings")

