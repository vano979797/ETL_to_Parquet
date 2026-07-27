import logging
import sys
from pathlib import Path

# TODO прокинуть адреса через модули, для унификации импортов
from source_eng.extract import load_all
from source_eng.transform import clean_csv, clean_json, clean_excel, merge_data
from source_eng.analysis import run_analytics
from source_eng.load import save_clean_data, save_analysis


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/etl.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('etl_pipeline')

def run_etl(raw_dir: str = 'data/raw', processed_dir: str = 'data/processed') -> None:
    """
    Запускает полный ETL-пайплайн.
    """
    logger.info("Запуск ETL!")

    try:
        logger.info(f"Чтение данных из {raw_dir}")
        csv_df, json_df, excel_df = load_all(raw_dir)
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
        logger.info(f"Результаты сохранены в {processed_dir}")

    except Exception as e:
        logger.error(f"Ошибка в ETL: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ETL пайплайн для игр')
    parser.add_argument('--raw', default='data/raw', help='Папка с исходными данными')
    parser.add_argument('--processed', default='data/processed', help='Папка для сохранения результатов')
    args = parser.parse_args()

    run_etl(args.raw, args.processed)