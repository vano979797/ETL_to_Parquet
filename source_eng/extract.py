from pathlib import Path

import pandas as pd

from .config import DEFAULT_CONFIG


def read_csv(filepath:str | Path) -> pd.DataFrame:
    return pd.read_csv(filepath)

def read_json(filepath:str | Path) -> pd.DataFrame:
    return pd.read_json(filepath)

def read_excel(filepath:str | Path) -> pd.DataFrame:
    return pd.read_excel(filepath)

def load_all( prefix='',config = DEFAULT_CONFIG) -> tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    """
    Загружает все три источника данных из указанной папки.

    Args:
        prefix (str): Префикс для имён файлов (например, 'g_' для сгенерированных).

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Кортеж из трёх датафреймов:
            - CSV (полный набор данных)
            - JSON (дополнительные атрибуты)
            - Excel (продажи по регионам)

    Raises:
        FileNotFoundError: Если какой-либо из требуемых файлов отсутствует.
    """
    base = config.raw_dir
    csv_path = base / f'{prefix}games.csv'
    json_path = base / f'{prefix}games.json'
    excel_path = base / f'{prefix}games_sales.xlsx'


    if not csv_path.exists():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")
    if not json_path.exists():
        raise FileNotFoundError(f"JSON файл не найден: {json_path}")
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel файл не найден: {excel_path}")

    csv_df = read_csv(base/f'{prefix}games.csv')
    json_df = read_json(base/f'{prefix}games.json')
    excel_df = read_excel(base/f'{prefix}games_sales.xlsx')
    return csv_df, json_df, excel_df