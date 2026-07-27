from source_eng.extract import load_all

def main():
    csv_df,json_df,excel_df = load_all()
    print("CSV shape:", csv_df.shape)
    print(csv_df.head())
    print("\nJSON shape:", json_df.shape)
    print(json_df.head())
    print("\nExcel shape:", excel_df.shape)
    print(excel_df.head())

if __name__ == '__main__':
    main()

#скрипт длят запуска
# python -m scripts.test_extract
