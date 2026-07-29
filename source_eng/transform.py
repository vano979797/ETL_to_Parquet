import pandas as pd

from .config import (
    COLUMN_ORDER,
    CRITIC_SCORE_RANGE,
    SALES_COLS,
    STRING_COLS,
    USER_SCORE_RANGE,
)


def _clean_sales(df: pd.DataFrame, sales_cols: tuple) -> pd.DataFrame:
    """Приводит колонки продаж к числовым, заполняет пропуски нулём, обрезает отрицательные."""
    for col in sales_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df[col] = df[col].clip(lower=0)
    return df

def _clean_scores(
        df: pd.DataFrame,
        score_col: str,
        min_val: int,
        max_val: int,
        group_by_col: str | None = None
) -> pd.DataFrame:
    """Очищает колонку с оценкой: приводит к числу, заполняет пропуски (по группе или глобально), обрезает."""
    df[score_col] = pd.to_numeric(df[score_col], errors='coerce')

    if group_by_col and group_by_col in df.columns:
        df[score_col] = df.groupby(group_by_col)[score_col].transform(lambda x: x.fillna(x.mean()))

    if df[score_col].isna().any():
        df[score_col] = df[score_col].fillna(df[score_col].mean())
    df[score_col] = df[score_col].clip(min_val, max_val)

    return df

def _clean_strings(df: pd.DataFrame, string_cols: tuple) -> pd.DataFrame:
    """Удаляет пробелы по краям в строковых колонках."""
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

def _deduplicate_by_name(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет дубликаты по колонке Name, оставляя первую запись."""
    if 'Name' in df.columns:
        df = df.drop_duplicates(subset=['Name'], keep='first')

    return df

def clean_csv(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Год выпуска
    df['Year_of_Release'] = pd.to_numeric(df['Year_of_Release'], errors='coerce')
    df['Year_of_Release'] = df['Year_of_Release'].fillna(df['Year_of_Release'].median()).astype(int)

    # Оценки с группировкой по жанру
    df = _clean_scores(df, 'Critic_Score', *CRITIC_SCORE_RANGE, group_by_col='Genre')
    df = _clean_scores(df, 'User_Score', *USER_SCORE_RANGE, group_by_col='Genre')

    # Продажи
    df = _clean_sales(df, SALES_COLS)

    # Строки и дубликаты
    df = _clean_strings(df, STRING_COLS)
    df = _deduplicate_by_name(df)

    return df

def clean_json(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'Critic_Score' in df.columns:
        df = _clean_scores(df, 'Critic_Score', *CRITIC_SCORE_RANGE)
    if 'User_Score' in df.columns:
        df = _clean_scores(df, 'User_Score', *USER_SCORE_RANGE)
    df = _clean_strings(df, STRING_COLS)
    df = _deduplicate_by_name(df)

    return df

def clean_excel(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    sales_present = [col for col in SALES_COLS if col in df.columns]
    if sales_present:
        df = _clean_sales(df, sales_present)
    df = _clean_strings(df, STRING_COLS)
    df = _deduplicate_by_name(df)

    return df

def merge_data(
        csv_df: pd.DataFrame,
        json_df: pd.DataFrame,
        excel_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Объединяет три источника данных в один датафрейм.
    - Сначала LEFT JOIN csv с json по id.
    - Затем LEFT JOIN с excel по id.
    - Заполняет пропуски в discount нулём.
    - Вычисляет final_price = price * (1 - discount/100).
    """

    for df in [csv_df, json_df, excel_df]:
        if 'Name' not in df.columns:
            raise ValueError("Один из датафреймов не содержит колонку 'Name'")

    merged = csv_df.copy()

    json_cols_to_merge = [col for col in json_df.columns if col != 'Name' and col in merged.columns]

    if json_cols_to_merge:
        merged = pd.merge(merged, json_df[['Name'] + json_cols_to_merge], on='Name', how='left', suffixes=('', '_json'))
        for col in json_cols_to_merge:
            if f"{col}_json" in merged.columns:
                merged[col] = merged[col].fillna(merged[f"{col}_json"])
                merged.drop(columns=[f"{col}_json"], inplace=True)

    excel_cols_to_merge = [col for col in excel_df.columns if col != 'Name' and col in merged.columns]

    if excel_cols_to_merge:
        merged = pd.merge(merged, excel_df[['Name'] + excel_cols_to_merge], on='Name', how='left',
                          suffixes=('', '_excel'))
        for col in excel_cols_to_merge:
            if f"{col}_excel" in merged.columns:
                merged[col] = merged[col].fillna(merged[f"{col}_excel"])
                merged.drop(columns=[f"{col}_excel"], inplace=True)

    for col in SALES_COLS:
        if col not in merged.columns:
            merged[col] = 0
    merged['Total_sales'] = merged[list(SALES_COLS)].sum(axis=1).round(2)

    final_columns = [col for col in COLUMN_ORDER if col in merged.columns]
    merged = merged[final_columns]

    return merged