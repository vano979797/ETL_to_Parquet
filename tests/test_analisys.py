from source_eng.analysis import run_analytics


def test_run_analytics(sample_csv_data):
    # Нам нужен объединённый DataFrame, поэтому используем фикстуры, но для простоты создадим полный df
    df = sample_csv_data.copy()
    # Добавим Total_sales для теста
    df['Total_sales'] = df[['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']].sum(axis=1)
    # Заполним пропуски, чтобы аналитика не упала
    df['Critic_Score'] = df['Critic_Score'].fillna(0)
    df['User_Score'] = df['User_Score'].fillna(0)

    results = run_analytics(df)
    assert 'genre_stats' in results
    assert 'top_sales' in results
    assert 'top_critic' in results
    assert not results['genre_stats'].empty
    assert not results['top_sales'].empty
    assert not results['top_critic'].empty
