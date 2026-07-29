import argparse
from datetime import datetime, timezone
import logging
from pathlib import Path
import sys

from scripts.generate_data import gen_data
from source_eng.analysis import run_analytics
from source_eng.config import DEFAULT_CONFIG
from source_eng.extract import load_all
from source_eng.load import save_analysis, save_clean_data
from source_eng.transform import clean_csv, clean_excel, clean_json, merge_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/etl.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('etl_pipeline')


def check_file_exists(prefix: str = '', raw_dir: str | Path = DEFAULT_CONFIG.raw_dir) -> bool:
    """
    Проверяет наличие всех трёх файлов с указанным префиксом в папке data/raw.

    Args:
        prefix (str): Префикс имени файлов (например, '' или 'g_').

    Returns:
        bool: True, если все три файла существуют, иначе False.
    """
    raw_dir = Path(raw_dir)
    required_files = [
        f'{prefix}games.csv',
        f'{prefix}games.json',
        f'{prefix}games_sales.xlsx'
    ]
    for fname in required_files:
        if not (raw_dir / fname).exists():
            logger.debug(f"Файл не найден: {raw_dir / fname}")
            return False
    return True

def resolve_mode(mode: str, has_local: bool, has_gen: bool) -> tuple[str, bool]:
    """Определяет префикс и нужно ли генерировать данные."""
    if mode == 'local':
        if not has_local:
            logger.error("❌ Режим 'local' выбран, но файлы без префикса не найдены")
            sys.exit(1)
        return '', False
    if mode == 'gen':
        return 'g_', True
    # auto
    if has_local:
        logger.info("Авторежим: найдены локальные файлы")
        return '', False
    logger.info("Авторежим: локальные файлы не найдены, генерируем")
    return 'g_', True

def run_etl(
        raw_dir: str | Path = DEFAULT_CONFIG.raw_dir,
        processed_dir: str | Path = DEFAULT_CONFIG.processed_dir,
        prefix: str = '',
        mode: str = 'auto'
) -> None:
    """
    Запускает полный ETL-пайплайн. C с указанием режима в виде прификса.
    Args:
        prefix (str): Префикс для имён файлов (например, 'g_' - генеренные).
    """
    logger.info("Запуск ETL!")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir) / timestamp
    processed_dir.mkdir(parents=True, exist_ok=False)
    logger.info(f"Результаты будут сохранены в {processed_dir}")

    with open(processed_dir / "run_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Run timestamp: {timestamp}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Prefix: {prefix}\n")
        f.write(f"Raw data dir: {raw_dir}\n")

    try:
        logger.info(f"Чтение данных из {raw_dir}")
        csv_df, json_df, excel_df = load_all(prefix=prefix)
        logger.info(f"CSV: {len(csv_df)} строк, JSON: {len(json_df)} строк, Excel: {len(excel_df)} строк")

        logger.info("Очистка данных ...")
        csv_clean = clean_csv(csv_df)
        json_clean = clean_json(json_df)
        excel_clean = clean_excel(excel_df)
        logger.info(f"После очистки: CSV={len(csv_clean)}, JSON={len(json_clean)}, Excel={len(excel_clean)}")

        logger.info("Объединение данных...")
        merged = merge_data(csv_clean,json_clean,excel_clean)
        logger.info(f"После объединения: {len(merged)} строк")

        logger.info("Анализ ...")
        results = run_analytics(merged)
        for name, df in results.items():
            logger.info(f"  - {name}: {len(df)} записей")

        logger.info(f"Сохранение данных в {processed_dir}")
        save_clean_data(merged,processed_dir)
        save_analysis(results,processed_dir)

        logger.info("ETL-пайплайн завершён успешно!")
        logger.info(f"Результаты сохранены в {processed_dir} под названием games_clean.parquet")

        logger.info("✅ ETL-пайплайн завершён успешно!")


    except Exception:
        logger.exception("Ошибка в ETL")
        raise

def main():
    parser = argparse.ArgumentParser(
        description='ETL пайплайн для данных игр. Поддерживает работу с пользовательскими и сгенерированными данными.'
    )
    parser.add_argument(
        '--mode',
        choices=['auto', 'gen', 'local'],
        default='auto',
        help="Режим работы: auto (автоопределение,проверяет наличие файлов в папке), "
             "generate (сгенерировать новые данные), "
             "local (использовать свои файлы)"
    )
    parser.add_argument(
        '--raw',
        default='data/raw',
        help='Папка с исходными данными'
    )
    parser.add_argument(
        '--processed',
        default='data/processed',
        help='Папка для сохранения результатов'
    )
    args = parser.parse_args()

    mode = args.mode
    raw_dir = args.raw
    processed_dir = args.processed
    logger.info(f"Выбран режим: {mode}")

    has_local = check_file_exists(prefix='', raw_dir=raw_dir)
    has_gen = check_file_exists(prefix='g_', raw_dir=raw_dir)

    logger.debug(f"Наличие локальных файлов: {has_local}")
    logger.debug(f"Наличие сгенерированных файлов: {has_gen}")

    prefix, may_gen = resolve_mode(mode,has_local,has_gen)

    if may_gen:
        logger.info("Генерация новых данных...")
        gen_data()  # создаёт файлы с префиксом 'g_'

    run_etl(
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        prefix=prefix,
        mode=mode,
    )

if __name__ == '__main__':
    main()
