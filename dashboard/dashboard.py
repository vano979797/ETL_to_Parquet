import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Настройка страницы
st.set_page_config(
    page_title="Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Аналитика продаж игр")
st.markdown("---")


# --- Функция загрузки данных ---
@st.cache_data
def load_data():
    processed_base = Path("data/processed")
    if not processed_base.exists():
        st.error("Папка data/processed не найдена. Сначала запустите ETL-пайплайн.")
        return None, None

    # Находим самую свежую папку с результатами (по дате создания)
    run_dirs = [d for d in processed_base.iterdir() if d.is_dir()]
    if not run_dirs:
        st.error("В data/processed нет папок с результатами. Запустите ETL.")
        return None, None

    latest_run = max(run_dirs, key=lambda d: d.stat().st_ctime)

    # Загружаем файлы
    games_path = latest_run / "games_clean.parquet"
    genre_stats_path = latest_run / "genre_stats.parquet"

    if not games_path.exists():
        st.error(f"Файл {games_path} не найден.")
        return None, None

    games_df = pd.read_parquet(games_path)
    genre_stats = pd.read_parquet(genre_stats_path) if genre_stats_path.exists() else None

    return games_df, genre_stats, latest_run.name


games_df, genre_stats, run_name = load_data()

if games_df is None:
    st.stop()

st.sidebar.header("Информация о данных")
st.sidebar.write(f"Запуск: {run_name}")
st.sidebar.write(f"Всего игр: {len(games_df)}")

# --- Фильтры ---
st.sidebar.header("Фильтры")
all_genres = ["Все"] + sorted(games_df['Genre'].unique())
selected_genre = st.sidebar.selectbox("Жанр", all_genres)

# Фильтр по году (ползунок)
min_year = int(games_df['Year_of_Release'].min())
max_year = int(games_df['Year_of_Release'].max())
year_range = st.sidebar.slider(
    "Год выпуска",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Фильтр по платформе
platforms = ["Все"] + sorted(games_df['Platform'].unique())
selected_platform = st.sidebar.selectbox("Платформа", platforms)

# Применяем фильтры
filtered_df = games_df.copy()
if selected_genre != "Все":
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]
if selected_platform != "Все":
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]
filtered_df = filtered_df[
    (filtered_df['Year_of_Release'] >= year_range[0]) &
    (filtered_df['Year_of_Release'] <= year_range[1])
    ]

# --- Основные метрики (KPI) ---
st.subheader("📊 Ключевые показатели")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего игр", len(filtered_df))
col2.metric("Средний рейтинг критиков", f"{filtered_df['Critic_Score'].mean():.1f}")
col3.metric("Средние продажи (млн)", f"{filtered_df['Total_sales'].mean():.2f}")
col4.metric("Суммарные продажи (млн)", f"{filtered_df['Total_sales'].sum():.2f}")

st.markdown("---")

# --- Графики ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Топ-10 игр по продажам")
    top_games = filtered_df.nlargest(10, 'Total_sales')
    fig = px.bar(
        top_games,
        x='Total_sales',
        y='Name',
        orientation='h',
        color='Genre',
        title="Топ-10 по общим продажам",
        labels={'Total_sales': 'Продажи (млн)', 'Name': ''},
        height=500
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📈 Продажи по жанрам")
    genre_sales = filtered_df.groupby('Genre')['Total_sales'].sum().reset_index()
    fig = px.pie(
        genre_sales,
        values='Total_sales',
        names='Genre',
        title="Доля продаж по жанрам",
        hole=0.4,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Второй ряд графиков
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("⭐ Оценки критиков vs пользователей")
    fig = px.scatter(
        filtered_df,
        x='Critic_Score',
        y='User_Score',
        color='Genre',
        size='Total_sales',
        hover_data=['Name'],
        title="Сравнение оценок",
        labels={'Critic_Score': 'Оценка критиков', 'User_Score': 'Оценка пользователей'},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right2:
    st.subheader("🌍 Продажи по регионам")
    region_sales = filtered_df[['NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']].sum()
    region_sales = region_sales.reset_index()
    region_sales.columns = ['Регион', 'Продажи']
    fig = px.bar(
        region_sales,
        x='Регион',
        y='Продажи',
        title="Суммарные продажи по регионам",
        labels={'Продажи': 'Продажи (млн)'},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Дополнительная таблица
st.markdown("---")
st.subheader("📋 Данные с фильтрацией")
st.dataframe(filtered_df, use_container_width=True)