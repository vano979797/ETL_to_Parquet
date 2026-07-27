import pandas as pd
from pathlib import Path


def read_csv(filepath:str | Path) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=['release_date'])

def read_json(filepath:str | Path) -> pd.DataFrame:
    return pd.read_json(filepath)

def read_excel(filepath:str | Path) -> pd.DataFrame:
    return pd.read_excel(filepath, parse_dates=['start_date','end_date'])

def load_all(base_dir:str | Path = 'data/raw') -> tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    base = Path(base_dir)
    csv_df = read_csv(base/'games.csv')
    json_df = read_json(base/'games.json')
    excel_df = read_excel(base/'discounts.xlsx')
    return csv_df, json_df, excel_df