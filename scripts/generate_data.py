import pandas as pd
import json
from pathlib import Path
import random
from datetime import datetime, timedelta


def main():
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

    num_req = len(game_names)

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
            "Rating": rating
        })

        df = pd.DataFrame(records)

        df.to_csv('data/raw/games.csv', index=False, encoding='utf-8')



        # Name, Platform, Year_of_Release, Genre, NA_sales, EU_sales, JP_sales, Other_sales, Critic_Score, User_Score, Rating

#     csv_data = """id,title,genre,price,release_date,stock
# 1,Cyberpunk 2077,RPG,59.99,2020-12-10,45
# 2,The Witcher 3,RPG,39.99,2015-05-19,30
# 3,Stardew Valley,Simulation,14.99,2016-02-26,60
# 4,Hades,Action,24.99,2020-09-17,50
# 5,Civilization VI,Strategy,59.99,2016-10-21,20
# 6,Doom Eternal,Shooter,39.99,2020-03-20,35
# 7,Disco Elysium,RPG,39.99,2019-10-15,15
# 8,Hollow Knight,Platformer,14.99,2017-02-24,80
# 9,Factorio,Simulation,30.00,2020-08-14,25
# 10,Ori and the Will of the Wisps,Platformer,29.99,2020-03-11,40"""
    with open('data/raw/games.csv','w', encoding='UTF-8') as f:
        f.write(csv_data)

    json_data = [
        {"id": 1, "developer": "CD Projekt Red", "players": 25000000, "rating": 4.8},
        {"id": 2, "developer": "CD Projekt Red", "players": 30000000, "rating": 4.9},
        {"id": 3, "developer": "ConcernedApe", "players": 15000000, "rating": 4.9},
        {"id": 4, "developer": "Supergiant Games", "players": 5000000, "rating": 4.8},
        {"id": 5, "developer": "Firaxis", "players": 8000000, "rating": 4.6},
        {"id": 6, "developer": "id Software", "players": 6000000, "rating": 4.7},
        {"id": 7, "developer": "ZA/UM", "players": 2000000, "rating": 4.7},
        {"id": 8, "developer": "Team Cherry", "players": 5000000, "rating": 4.8},
        {"id": 10, "developer": "Moon Studios", "players": 3000000, "rating": 4.6}
    ]
    with open('data/raw/games.json','w',encoding='UTF-8') as f:
        json.dump(json_data,f,indent=2,ensure_ascii=False)

    excel_data = [
        [2, 20, '2023-11-01', '2023-11-30'],
        [3, 10, '2023-10-15', '2023-10-31'],
        [5, 30, '2023-11-20', '2023-12-05'],
        [7, 15, '2023-11-01', '2023-11-15'],
        [11, 25, '2023-12-01', '2023-12-31']
    ]

    df_excel = pd.DataFrame(excel_data, columns=['id', 'discount', 'start_date', 'end_date'])
    df_excel.to_excel('data/raw/discounts.xlsx', index=False)

    print("✅ Тестовые данные созданы в data/raw/")

if __name__ == '__main__':
    main()