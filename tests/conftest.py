import pytest
import pandas as pd

@pytest.fixture
def sample_csv_data():
    """Создаёт небольшой DataFrame, имитирующий CSV."""
    return pd.DataFrame({
        "Name": ["Game1", "Game2", "Game3"],
        "Platform": ["PC", "PS4", "Switch"],
        "Year_of_Release": [2020, 2021, 2019],
        "Genre": ["Action", "RPG", "Action"],
        "NA_sales": [1.2, 0.8, 2.1],
        "EU_sales": [0.9, 1.1, 1.5],
        "JP_sales": [0.1, 0.3, 0.4],
        "Other_sales": [0.4, 0.5, 0.6],
        "Critic_Score": [88, 92, None],
        "User_Score": [8.5, 9.0, None],
        "Rating": ["E", "M", "E10+"]
    })

@pytest.fixture
def sample_json_data():
    """Имитирует JSON-данные (частичные)."""
    return pd.DataFrame({
        "Name": ["Game1", "Game2", "Game4"],
        "Platform": ["PC", "PS4", "Xbox"],
        "Critic_Score": [85, None, 78],
        "User_Score": [7.5, 8.2, None]
    })

@pytest.fixture
def sample_excel_data():
    """Имитирует Excel-данные (продажи)."""
    return pd.DataFrame({
        "Name": ["Game1", "Game2", "Game3"],
        "NA_sales": [1.0, None, 2.0],
        "EU_sales": [0.8, 0.9, None],
        "JP_sales": [0.2, 0.3, 0.1],
        "Other_sales": [0.3, 0.4, 0.5]
    })