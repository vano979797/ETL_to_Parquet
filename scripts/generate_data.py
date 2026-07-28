import pandas as pd
from pathlib import Path

import random


def clean_gen_data() -> bool:
    """
    Удаляет все файлы с префиксом 'g_' в папке data/raw.
    """
    raw_dir = Path('data/raw')
    if not raw_dir.exists():
        return
    for file_path in raw_dir.glob('g_*'):
        try:
            file_path.unlink()
            print(f"Удалён файл: {file_path}")
        except Exception as e:
            print(f"Не удалось удалить {file_path}: {e}")

def gen_data():
    """
    Генерирует случайные данные и сохраняет их в data/raw/ с префиксом 'g_'.
    Перед генерацией удаляет старые сгенерированные файлы.
    """
    clean_gen_data()
    Path('data/raw').mkdir(parents=True,exist_ok=True)
    Path('data/processed').mkdir(parents=True,exist_ok=True)

    game_names = [
        "Cyberpunk 2077", "The Witcher 3", "Stardew Valley", "Hades",
        "Civilization VI", "Doom Eternal", "Disco Elysium", "Hollow Knight",
        "Factorio", "Ori and the Will of the Wisps", "Minecraft", "Grand Theft Auto V",
        "Red Dead Redemption 2", "The Legend of Zelda: Breath of the Wild",
        "Super Mario Odyssey", "Pokemon Sword/Shield", "FIFA 20", "Animal Crossing",
        "Call of Duty: Modern Warfare", "Half-Life: Alyx",
        "Grand Theft Auto V", "Call of Duty: Modern Warfare", "Minecraft",
        "The Legend of Zelda: Breath of the Wild", "Red Dead Redemption 2",
        "Super Mario Odyssey", "The Witcher 3: Wild Hunt", "Pokemon Sword/Shield",
        "FIFA 20", "Hades", "Animal Crossing: New Horizons", "Cyberpunk 2077",
        "Doom Eternal", "Stardew Valley", "Disco Elysium", "Half-Life: Alyx",
        "Among Us", "Fall Guys", "Valorant", "League of Legends",
        "Elden Ring", "Horizon Forbidden West", "God of War", "Spider-Man",
        "Final Fantasy VII Remake", "Resident Evil Village", "Death Stranding",
        "Ghost of Tsushima", "The Last of Us Part II", "Uncharted 4"
    ]
    genres = ["RPG", "Action", "Simulation", "Strategy", "Shooter", "Platformer", "Adventure"]
    developers = [
        "CD Projekt Red", "ConcernedApe", "Supergiant Games", "Firaxis",
        "id Software", "ZA/UM", "Team Cherry", "Moon Studios", "Mojang",
        "Rockstar Games", "Nintendo", "Game Freak", "EA Sports", "Valve"
    ]
    platforms = [
        'PS4', 'PS5', 'Xbox One', 'Xbox Series X', 'PC', 'Switch',
        'Wii U', 'PS3', 'Xbox 360', 'DS', '3DS', 'PSP', 'Vita',
        'Stadia', 'Mac', 'Linux', 'Mobile', 'Dreamcast', 'GameCube', 'NES', 'Wii'
    ]
    ratings = ['E', 'E10+', 'T', 'M', 'AO']

    records = []

    for i,name in enumerate(game_names,1):
        platform = random.choice(platforms)
        year_of_release = random.randint(2000,2025)
        genre = random.choice(genres)
        na_sales = round(random.uniform(0,12),2)
        eu_sales = round(random.uniform(0,9),2)
        jp_sales = round(random.uniform(0,6),2)
        other_sales = round(random.uniform(0,5),2)
        critic_score = random.randint(0,100) if random.random() > 0.15 else None
        user_score = round(random.uniform(0,10),1) if random.random() > 0.15 else None
        rating = random.choice(ratings)
        developers = random.choice(developers)

        records.append({
            "Name": name,
            "Platform": platform,
            "Year_of_Release": year_of_release,
            "Genre": genre,
            "NA_sales": na_sales,
            "EU_sales": eu_sales,
            "JP_sales": jp_sales,
            "Other_sales": other_sales,
            "Critic_Score": critic_score,
            "User_Score": user_score,
            "Rating": rating,
            "Developers": developers
        })

        df = pd.DataFrame(records)

        df.to_csv('data/raw/g_games.csv', index=False, encoding='utf-8')

        json_subset = df[['Name', 'Platform', 'Critic_Score', 'User_Score']]
        json_subset.to_json('data/raw/g_games.json', orient='records',indent=2,force_ascii=False)

        excel_subset = df[['Name', 'NA_sales', 'EU_sales', 'JP_sales', 'Other_sales']]
        excel_subset.to_excel('data/raw/g_games_sales.xlsx')

        print(f"✅ Сгенерировано {len(records)} записей в data/raw/")
        print(f"  - games.csv: все колонки ({len(df)} записей)")
        print(f"  - games.json: Name, Platform, Critic_Score, User_Score")
        print(f"  - games_sales.xlsx: Name, NA_sales, EU_sales, JP_sales, Other_sales")


