from pathlib import Path

import pandas as pd

from source_eng.extract import load_all
from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data
from source_eng.analysis import run_analytics
from source_eng.load import save_clean_data, save_analysis


def main():
    csv_df, json_df, excel_df = load_all()

    csv_clean = clean_csv(csv_df)
    json_clean = clean_json(json_df)
    excel_clean = clean_excel(excel_df)
    merged = merge_data(csv_clean, json_clean, excel_clean)

    results = run_analytics(merged)

    save_clean_data(merged)
    save_analysis(results)

    print("✅ Все данные сохранены в data/processed/")
    print("Файлы:")
    for f in Path('data/processed').glob('*.parquet'):
        print(f"  - {f.name}")

    print("\nПроверка: чтение сохранённого clean-файла")
    df_check = pd.read_parquet('data/processed/games_clean.parquet')
    print(df_check.head())



if __name__ == '__main__':
    main()