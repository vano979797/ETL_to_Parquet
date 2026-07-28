import duckdb
import pandas as pd

def run_analytics(df: pd.DataFrame) -> dict:
    """
    Выполняет SQL-аналитику над объединённым датафреймом.
    Возвращает словарь с тремя витринами (DataFrame):
      - genre_stats: статистика по жанрам (количество, средние продажи, средние оценки)
      - top_sales: топ-10 игр по общим продажам
      - top_critic: топ-10 игр по оценке критиков
    """
    # Регистрируем датафрейм в DuckDB
    duckdb.register('games', df)

    # 1. Статистика по жанрам
    genre_stats = duckdb.sql("""
        SELECT
            Genre,
            COUNT(*) AS game_count,
            AVG(NA_sales) AS avg_na_sales,
            AVG(EU_sales) AS avg_eu_sales,
            AVG(JP_sales) AS avg_jp_sales,
            AVG(Other_sales) AS avg_other_sales,
            AVG(Total_sales) AS avg_total_sales,
            AVG(Critic_Score) AS avg_critic_score,
            AVG(User_Score) AS avg_user_score,
            AVG(Critic_Score - User_Score*10) AS avg_score_diff
        FROM games
        GROUP BY Genre
        ORDER BY avg_total_sales DESC
    """).df()

    # 2. Топ-10 игр по общим продажам
    top_sales = duckdb.sql("""
        SELECT
            Name,
            Platform,
            Genre,
            Total_sales,
            NA_sales,
            EU_sales,
            JP_sales,
            Other_sales,
            Critic_Score,
            User_Score,
            Rating
        FROM games
        ORDER BY Total_sales DESC
        LIMIT 10
    """).df()

    # 3. Топ-10 игр по оценке критиков (с фильтром, что оценка не NULL и есть продажи)
    top_critic = duckdb.sql("""
        SELECT
            Name,
            Platform,
            Genre,
            Critic_Score,
            User_Score,
            Total_sales,
            Rating
        FROM games
        WHERE Critic_Score IS NOT NULL
        ORDER BY Critic_Score DESC
        LIMIT 10
    """).df()

    # Возвращаем словарь с результатами
    return {
        'genre_stats': genre_stats,
        'top_sales': top_sales,
        'top_critic': top_critic
    }