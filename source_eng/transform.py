import pandas as pd


def clean_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из CSV-файла.
    - Заполняет пропуски в stock нулём.
    - Приводит price к float.
    - Удаляет дубликаты по id.
    """
    df = df.copy()
    df['Year_of_Release'] = pd.to_numeric(df['Year_of_Release'], errors='coerce')
    median_year = df['Year_of_Release'].median()
    df['Year_of_Release'] = df['Year_of_Release'].fillna(median_year).astype(int)

    df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce')
    df['Critic_Score'] = df.groupby('Genre')['Critic_Score'].transform(
        lambda x: x.fillna(x.mean())
    )
    overall_mean_critic = df['Critic_Score'].mean()
    df['Critic_Score'] = df['Critic_Score'].fillna(overall_mean_critic)
    df['Critic_Score'] = df['Critic_Score'].clip(0, 100).round().astype(int)

    df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
    df['User_Score'] = df.groupby('Genre')['User_Score'].transform(
        lambda x: x.fillna(x.mean())
    )
    overall_mean_user = df['User_Score'].mean()
    df['User_Score'] = df['User_Score'].fillna(overall_mean_user)
    df['User_Score'] = df['User_Score'].clip(0, 10).round(1)

    sales_cols = ['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']
    for col in sales_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df[col] = df[col].clip(lower=0)

    df = df.drop_duplicates(subset=['Name'], keep='first')

    string_cols = ['Name', 'Platform', 'Genre', 'Rating']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

# Name,Platform,Year_of_Release,Genre,NA_sales,EU_sales,JP_sales,Other_sales,Critic_Score,User_Score,Rating

def clean_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из JSON.
    - Заполняет пропуски в rating значением 3.0.
    - Приводит players к int.
    """
    df = df.copy()

    if 'Critic_Score' in df.columns:
        df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce')
        df['Critic_Score'] = df['Critic_Score'].fillna(df['Critic_Score'].mean())
        df['Critic_Score'] = df['Critic_Score'].clip(0, 100).round().astype(int)

    if 'User_Score' in df.columns:
        df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
        df['User_Score'] = df['User_Score'].fillna(df['User_Score'].mean())
        df['User_Score'] = df['User_Score'].clip(0, 10).round(1)

    if 'Name' in df.columns:
        df = df.drop_duplicates(subset=['Name'], keep='first')
        df['Name'] = df['Name'].astype(str).str.strip()

    return df

def clean_excel(df:pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных из Excel.
    - Ограничивает discount диапазоном [0, 100].
    - Заполняет пропуски в discount нулём.
    """
    df = df.copy()
    sales_cols = ['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']
    for col in sales_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            df[col] = df[col].clip(lower=0)

    # Удаляем дубликаты по Name
    if 'Name' in df.columns:
        df = df.drop_duplicates(subset=['Name'], keep='first')
        df['Name'] = df['Name'].astype(str).str.strip()

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

    sales_cols = ['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']
    for col in sales_cols:
        if col not in merged.columns:
            merged[col] = 0
    merged['Total_sales'] = merged[sales_cols].sum(axis=1).round(2)

    column_order = ['Name', 'Platform', 'Year_of_Release', 'Genre',
                    'NA_sales', 'EU_sales', 'JP_sales', 'Other_sales', 'Total_sales',
                    'Critic_Score', 'User_Score', 'Rating']
    final_columns = [col for col in column_order if col in merged.columns]
    merged = merged[final_columns]
    return merged