import logging
import sys
import argparse
from pathlib import Path
from datetime import datetime

# TODO прокинуть адреса через модули, для унификации импортов
from source_eng.extract import load_all
from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data
from source_eng.analysis import run_analytics
from source_eng.load import save_clean_data, save_analysis
from scripts.generate_data import gen_data


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/etl.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('etl_pipeline')


def check_file_exists(prefix: str = '') -> bool:
    """
    Проверяет наличие всех трёх файлов с указанным префиксом в папке data/raw.

    Args:
        prefix (str): Префикс имени файлов (например, '' или 'g_').

    Returns:
        bool: True, если все три файла существуют, иначе False.
    """
    base = Path('data/raw')
    required_files = [
        f'{prefix}games.csv',
        f'{prefix}games.json',
        f'{prefix}games_sales.xlsx'
    ]
    for fname in required_files:
        if not (base / fname).exists():
            logger.debug(f"Файл не найден: {base / fname}")
            return False
    return True

def run_etl(
        raw_dir: str|Path = 'data/raw',
        processed_base: str = 'data/processed',
        prefix: str = '',
        mode: str = 'auto'
) -> None:
    """
    Запускает полный ETL-пайплайн. C с указанием режима в виде прификса.
    Args:
        prefix (str): Префикс для имён файлов (например, 'g_' - генеренные).
    """
    logger.info("Запуск ETL!")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    processed_dir = Path(processed_base) / timestamp
    processed_dir.mkdir(parents=True, exist_ok=False)
    logger.info(f"Результаты будут сохранены в {processed_dir}")

    with open(processed_dir / "run_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Run timestamp: {timestamp}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Prefix: {prefix}\n")

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

    except Exception as e:
        logger.error(f"Ошибка в ETL: {e}", exc_info=True)
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

    has_local = check_file_exists(prefix='')
    has_gen = check_file_exists(prefix='g_')

    logger.debug(f"Наличие локальных файлов: {has_local}")
    logger.debug(f"Наличие сгенерированных файлов: {has_gen}")

    if mode == 'local':
        if not has_local:
            logger.error("❌ Режим 'local' выбран, но файлы без префикса не найдены в data/raw/")
            sys.exit(1)
        prefix = ''
        logger.info("Используем локальные пользовательские файлы (без префикса)")
    elif mode == 'gen':
        logger.info("Режим 'generate': генерируем новые данные...")
        gen_data()
        prefix = 'g_'
        logger.info("Используем сгенерированные файлы (с префиксом 'g_')")
    else:
        # Выбран mode = auto
        if has_local:
            prefix = ''
            logger.info("Авторежим: найдены локальные файлы, используем их (без префикса)")
        else:
            gen_data()
            prefix = 'g_'
            logger.info("Используем сгенерированные файлы (с префиксом 'g_')")
    run_etl(raw_dir=raw_dir, processed_base=processed_dir,prefix=prefix,mode=mode)

if __name__ == '__main__':
    main()
