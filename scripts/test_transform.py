from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data
from source_eng.extract import load_all

def main():
    csv_df, json_df, excel_df = load_all()
    print(f"До очистки: CSV={len(csv_df)}, JSON={len(json_df)}, Excel={len(excel_df)}")

    csv_clean = clean_csv(csv_df)
    json_clean = clean_json(json_df)
    excel_clean = clean_excel(excel_df)

    print(f"После очистки: CSV={len(csv_clean)}, JSON={len(json_clean)}, Excel={len(excel_clean)}")

    merged = merge_data(csv_clean,json_clean,excel_clean)

    print(f"После объединения: {len(merged)} строк")
    print(merged.head())


if __name__ == '__main__':
    main()