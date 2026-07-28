import pandas as pd
import pytest
from pathlib import Path
from source_eng.load import save_parquet, save_clean_data, save_analysis

def test_save_parquet(tmp_path):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    filepath = tmp_path / "test.parquet"
    save_parquet(df, filepath)
    assert filepath.exists()
    loaded = pd.read_parquet(filepath)
    assert loaded.equals(df)

def test_save_clean_data(tmp_path, sample_csv_data):
    save_clean_data(sample_csv_data, output_dir=tmp_path)
    filepath = tmp_path / "games_clean.parquet"
    assert filepath.exists()
    loaded = pd.read_parquet(filepath)
    assert len(loaded) == len(sample_csv_data)

def test_save_analysis(tmp_path):
    results = {
        "test1": pd.DataFrame({"a": [1, 2]}),
        "test2": pd.DataFrame({"b": [3, 4]})
    }
    save_analysis(results, output_dir=tmp_path)
    for name in results.keys():
        assert (tmp_path / f"{name}.parquet").exists()
