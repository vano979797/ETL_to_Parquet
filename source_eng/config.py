from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    mandatory_columns: tuple = ("Name", "Platform", "Year_of_Release", "Genre")
    sales_columns: tuple = ("NA_sales", "EU_sales", "JP_sales", "Other_sales")
    critic_score_min: int = 0
    critic_score_max: int = 100
    user_score_min: int = 0
    user_score_max: int = 10
    duckdb_memory_limit: str = "1GB"

SALES_COLS = ('NA_sales', 'EU_sales', 'JP_sales', 'Other_sales')
STRING_COLS = ('Name', 'Platform', 'Genre', 'Rating')
CRITIC_SCORE_RANGE = (0, 100)
USER_SCORE_RANGE = (0, 10)
CRITICAL_COLS = ('Name', 'Platform', 'Year_of_Release', 'Genre')
COLUMN_ORDER = ['Name', 'Platform', 'Year_of_Release', 'Genre',
                    'NA_sales', 'EU_sales', 'JP_sales', 'Other_sales', 'Total_sales',
                    'Critic_Score', 'User_Score', 'Rating']

DEFAULT_CONFIG = Config()