from source_eng.extract import load_all
from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data
from source_eng.analysis import run_analytics


def main():
    csv_df, json_df, excel_df = load_all()

    csv_clean = clean_csv(csv_df)
    json_clean = clean_json(json_df)
    excel_clean = clean_excel(excel_df)

    merged = merge_data(csv_clean, json_clean, excel_clean)

    result = run_analytics(merged)

    for name, df in result.items():
        print(f"\n===== {name} =====")
        print(df)
        print(f"Rows: {len(df)}")




if __name__ == '__main__':
    main()