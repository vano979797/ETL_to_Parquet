import pytest
import pandas as pd
from pathlib import Path
from source_eng.extract import read_csv, read_json, read_excel, load_all


# Создаём временные файлы для тестов
@pytest.fixture
def temp_data_dir(tmp_path):
    data_dir = tmp_path / "data" / "raw"
    data_dir.mkdir(parents=True)

    # Сохраняем тестовый CSV
    csv_df = pd.DataFrame({"Name": ["Test"], "Platform": ["PC"]})
    csv_df.to_csv(data_dir / "games.csv", index=False)

    # JSON
    json_df = pd.DataFrame({"Name": ["Test"], "Critic_Score": [90]})
    json_df.to_json(data_dir / "games.json", orient="records")

    # Excel
    excel_df = pd.DataFrame({"Name": ["Test"], "NA_sales": [1.0]})
    excel_df.to_excel(data_dir / "games_sales.xlsx", index=False)

    return data_dir


def test_read_csv(temp_data_dir):
    df = read_csv(temp_data_dir / "games.csv")
    assert not df.empty
    assert "Name" in df.columns
    assert "Platform" in df.columns


def test_read_json(temp_data_dir):
    df = read_json(temp_data_dir / "games.json")
    assert not df.empty
    assert "Name" in df.columns
    assert "Critic_Score" in df.columns


def test_read_excel(temp_data_dir):
    df = read_excel(temp_data_dir / "games_sales.xlsx")
    assert not df.empty
    assert "Name" in df.columns
    assert "NA_sales" in df.columns


def test_load_all(temp_data_dir):
    csv_df, json_df, excel_df = load_all(base_dir=temp_data_dir, prefix='')
    assert len(csv_df) == 1
    assert len(json_df) == 1
    assert len(excel_df) == 1
