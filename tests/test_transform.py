import pandas as pd
import numpy as np
from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data

def test_clean_csv(sample_csv_data):
    cleaned = clean_csv(sample_csv_data)
    # Проверяем, что нет пропусков в колонках оценок
    assert cleaned['Critic_Score'].isnull().sum() == 0
    assert cleaned['User_Score'].isnull().sum() == 0
    # Проверяем диапазоны
    assert cleaned['Critic_Score'].between(0, 100).all()
    assert cleaned['User_Score'].between(0, 10).all()
    # Проверяем Year_of_Release int
    assert cleaned['Year_of_Release'].dtype == int
    # Проверяем, что дубликаты удалены
    assert len(cleaned) == len(cleaned['Name'].drop_duplicates())

def test_clean_json(sample_json_data):
    cleaned = clean_json(sample_json_data)
    if 'Critic_Score' in cleaned.columns:
        assert cleaned['Critic_Score'].isnull().sum() == 0
        assert cleaned['Critic_Score'].between(0, 100).all()
    if 'User_Score' in cleaned.columns:
        assert cleaned['User_Score'].isnull().sum() == 0
        assert cleaned['User_Score'].between(0, 10).all()

def test_clean_excel(sample_excel_data):
    cleaned = clean_excel(sample_excel_data)
    sales_cols = ['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']
    for col in sales_cols:
        if col in cleaned.columns:
            assert cleaned[col].isnull().sum() == 0
            assert (cleaned[col] >= 0).all()

def test_merge_data(sample_csv_data, sample_json_data, sample_excel_data):
    merged = merge_data(sample_csv_data, sample_json_data, sample_excel_data)
    assert 'Name' in merged.columns
    assert 'Total_sales' in merged.columns
    # Проверяем, что количество строк не уменьшилось (left join)
    assert len(merged) == len(sample_csv_data)
    # Проверяем, что оценки из JSON заполнили пропуски в CSV
    # Например, Game3 имел None в Critic_Score, но в merged должно быть значение
    assert merged[merged['Name'] == 'Game3']['Critic_Score'].iloc[0] is not None
