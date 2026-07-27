import duckdb
import pandas as pd


def run_analytics(df: pd.DataFrame) -> dict:
    """
    Выполняет SQL-аналитику над объединённым датафреймом.
    Возвращает словарь с несколькими витринами (DataFrame).
    """
    duckdb.register('games', df)

    genre_stats = duckdb.sql(
        """
        SELECT
            genre,
            COUNT(*) as count_games,
            AVG(price) as avg_price,
            AVG(final_price) as avg_discounted_price,
            SUM(stock) as total_stock,
            AVG(rating) as avg_rating,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM games
        GROUP BY genre
        ORDER BY avg_price DESC
        """
    ).df()

    top_expensive = duckdb.sql("""
            SELECT 
                title, 
                price, 
                developer,
                genre,
                rating
            FROM games
            ORDER BY price DESC
            LIMIT 5
        """).df()

    high_discount = duckdb.sql("""
            SELECT 
                title, 
                discount, 
                final_price,
                price,
                (price - final_price) as savings
            FROM games
            WHERE discount > 20
            ORDER BY discount DESC
        """).df()

    return {
        'genre_stats': genre_stats,
        'top_expensive': top_expensive,
        'high_discount': high_discount
    }