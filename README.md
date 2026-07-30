# 🎮 ETL-пайплайн для данных об играх

Проект представляет собой ETL-пайплайн для обработки данных о продажах игр из трёх источников (CSV, JSON, Excel) с последующей аналитикой и визуализацией в формате parquet.
# 📁 Структура проекта
```text

etl_games/
├── data/
│   ├── raw/                    # Исходные данные
│   │   ├── games.csv           # Основной файл (все колонки)
│   │   ├── games.json          # Дополнительные атрибуты
│   │   └── games_sales.xlsx    # Продажи по регионам
│   └── processed/              # Результаты (с версионированием по дате)
│       └── 20xx-xx-xx_xx-xx-xx/
│           ├── games_clean.parquet
│           ├── genre_stats.parquet
│           ├── top_sales.parquet
│           ├── top_critic.parquet
│           └── run_info.txt
├── dashboard/
│   ├── app.py                  # Streamlit-дашборд
│   ├── config.py               # Настройки дашборда
│   └── utils.py                # Вспомогательные функции
├── source_eng/
│   ├── config.py               # Конфигурация ETL
│   ├── extract.py              # Чтение данных
│   ├── transform.py            # Очистка и объединение
│   ├── analysis.py             # Аналитика (DuckDB)
│   └── load.py                 # Сохранение в Parquet
├── scripts/
│   └── generate_data.py        # Генерация тестовых данных
├── tests/                      # PyTest-тесты
├── logs/                       # Логи выполнения
├── main.py                     # Точка входа
├── requirements.txt
└── README.md
```
# 📦 Установка

Клонируй репозиторий:
```bash

    git clone <repo-url>
    cd etl_games
```
Создай виртуальное окружение:
```bash

    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
```
или
```shell
.venv\Scripts\activate  # Windows
```
Установи зависимости:
```bash
    pip install -r requirements.txt
```

Требования (requirements.txt):
```text
pandas
polars
duckdb
openpyxl
pyarrow
streamlit
plotly
pytest
ruff
```

# 🚀 Запуск ETL-пайплайна

Основной скрипт — `main.py`. Он поддерживает три режима работы и дополнительные аргументы для гибкой настройки.

## Режимы работы

| Режим | Флаг | Описание | Пример |
|-------|------|----------|--------|
| **Auto** (по умолчанию) | `--mode auto` | Проверяет наличие файлов в `data/raw`. Если есть — использует их. Если нет — генерирует новые. | `python main.py` |
| **Generate** | `--mode gen` | Всегда генерирует новые данные (файлы с префиксом `g_`) и запускает пайплайн. | `python main.py --mode gen` |
| **Local** | `--mode local` | Требует наличия пользовательских файлов в `data/raw`. Если их нет — завершается с ошибкой. | `python main.py --mode local` |

---

## Дополнительные аргументы

| Аргумент | Описание | Значение по умолчанию |
|----------|----------|-----------------------|
| `--raw` | Путь к папке с исходными данными | `data/raw` |
| `--processed` | Базовая папка для сохранения результатов | `data/processed` |

---

## 📌 Примеры запуска

```bash
# Авторежим (есть файлы — используем, нет — генерируем)
python main.py

# Принудительная генерация новых данных
python main.py --mode gen

# Использовать свои файлы
python main.py --mode local

# С указанием пользовательских путей
python main.py --mode gen --raw custom_data/raw --processed custom_data/processed
```


### Авторежим (есть файлы — используем, нет — генерируем)
```bash
python main.py
```
### Принудительная генерация новых данных
```bash
python main.py --mode gen
```
### Использовать свои файлы
```bash
python main.py --mode local
```
### С указанием своих папок
```bash
python main.py --mode gen --raw custom_data/raw --processed custom_data/processed
```
# 📊 Дашборд (визуализация)

После успешного выполнения ETL можно запустить интерактивный дашборд.
Запуск дашборда
```bash
streamlit run dashboard/app.py
```
Что доступно в дашборде

    Фильтры: по жанру, году выпуска, платформе.

    Ключевые метрики: общее количество игр, общие продажи, средние оценки.

    Графики:

        Продажи по жанрам (столбчатая диаграмма).

        Топ-5 игр по продажам.

        Распределение продаж по регионам (круговая диаграмма).

        Топ-5 игр по оценкам критиков.

Дашборд автоматически загружает данные из самой свежей папки в data/processed/.
🧪 Тестирование

Для запуска тестов используй pytest:
```bash
pytest tests/ -v
```
Проверка покрытия кода:
```bash
pytest tests/ --cov=source_eng
```
🔍 Формат данных
Исходные файлы

CSV (games.csv): полный набор данных.
```text
Name,Platform,Year_of_Release,Genre,NA_sales,EU_sales,JP_sales,Other_sales,Critic_Score,User_Score,Rating
```
JSON (games.json): подмножество колонок.
```json

{"Name": "Game", "Platform": "PC", "Critic_Score": 88, "User_Score": 8.5}
```
```
Excel (games_sales.xlsx): продажи по регионам.
Name	NA_sales	EU_sales	JP_sales	Other_sales
Game	1.2	0.9	0.1	0.4
```
# Результаты (Parquet)

После обработки создаются файлы:

    games_clean.parquet — объединённый и очищенный датафрейм.

    genre_stats.parquet — статистика по жанрам.

    top_sales.parquet — топ-10 игр по продажам.

    top_critic.parquet — топ-10 игр по оценкам критиков.

    run_info.txt — метаданные запуска.

# 🛠️ Модули
| Модуль | Назначение |
|--------|------------|
| `extract.py` | Чтение CSV, JSON, Excel. |
| `transform.py` | Очистка данных, объединение источников, расчёт `Total_sales`. |
| `analysis.py` | Аналитика через SQL (DuckDB). |
| `load.py` | Сохранение в Parquet. |
| `config.py` | Конфигурация (пути, колонки, диапазоны). |
| `generate_data.py` | Генерация случайных тестовых данных. |
| `app.py` | Streamlit-дашборд. |
# 🧹 Линтинг и форматирование

Проект использует Ruff для линтинга и форматирования.

# 📋 Логирование

Все логи сохраняются в logs/etl.log. Уровень логирования — INFO.
📌 Пример рабочего процесса

    Сгенерировать данные (если нет своих):
    bash

    python main.py --mode gen

    Запустить ETL с локальными файлами:
    bash

    python main.py --mode local

    Посмотреть результаты в дашборде:
    bash

    streamlit run dashboard/app.py

    Запустить тесты:
    bash

    pytest tests/ -v

🤝 Как добавить новый источник

    Добавь функцию чтения в extract.py.

    Добавь очистку в transform.py.

    При необходимости обнови merge_data.

    Если источник добавляет новые колонки — обнови config.py.
