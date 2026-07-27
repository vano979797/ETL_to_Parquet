import pandas as pd


def clean_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из CSV-файла.
    - Заполняет пропуски в stock нулём.
    - Приводит price к float.
    - Удаляет дубликаты по id.
    """
    df = df.copy()
    df['stock'] = df['stock'].fillna(0).astype(int)
    df['price'] = df['price'].astype(float)
    df = df.drop_duplicates(subset=['id'])
    return df

def clean_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из JSON.
    - Заполняет пропуски в rating значением 3.0.
    - Приводит players к int.
    """
    df = df.copy()
    df['rating'] = df['rating'].fillna(3.0)
    df['players'] = df['players'].fillna(0).astype(int)
    df = df.drop_duplicates(subset=['id'])
    return df

def clean_excel(df:pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из Excel.
    - Ограничивает discount диапазоном [0, 100].
    - Заполняет пропуски в discount нулём.
    """
    df = df.copy()
    df['discount'] = df['discount'].fillna(0).clip(0,100)
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
    merged = pd.merge(csv_df, json_df,on='id', how='left')
    merged = pd.merge(merged, excel_df,on='id', how='left')
    merged['discount'] = merged['discount'].fillna(0)
    merged['final_price'] = merged['price']*(1-merged['discount']/100)
    return merged