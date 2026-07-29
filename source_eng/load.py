import logging
from pathlib import Path

import pandas as pd

from .config import DEFAULT_CONFIG


logger = logging.getLogger(__name__)


def save_parquet(df: pd.DataFrame, filepath: str| Path) -> None:
    """
    Сохраняет DataFrame в формате Parquet.
    Создаёт папку, если её нет.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_parquet(path,index=False)

def save_clean_data(df:pd.DataFrame, output_dir:str|Path = 'data/processed') -> None:
    """ Сохраняет готовый паркет."""
    if output_dir is None:
        output_dir = DEFAULT_CONFIG.processed_dir
    save_parquet(df, Path(output_dir) / 'games_clean.parquet')

def save_analysis(result: dict,output_dir: str|Path = 'data/processed') -> None:
    """
    Сохраняет все аналитические витрины из словаря results.
    Ключи словаря = имена файлов (без расширения).
    """
    out_dir = Path(output_dir)
    for name, df in result.items():
        if isinstance(df, pd.DataFrame):
            save_parquet(df, out_dir / f"{name}.parquet")
        else:
            logger.warning(f"Пропущен ключ {name}: не является DataFrame")