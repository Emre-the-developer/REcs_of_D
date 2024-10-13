import pandas as pd
import sys
sys.path.append("C:/Users/emref/Desktop/C13digihome/REcs_of_D")
from Recs_of_D import Rec_title_check, registered_title_check

user_anime_df = pd.read_csv("C:/Users/emref/Desktop/processed_data2.csv")
user_anime_pivot = user_anime_df.pivot_table(index=["user_id"], columns=["Title"], values="user_score")
user_anime_pivot = user_anime_pivot.fillna(user_anime_pivot.mean())

# Yeni recommendation fonksiyonu
def second_anime_Recs(animeBase, user_name):
    prelist = []
    if animeBase in user_anime_pivot:
        anime_name = user_anime_pivot[animeBase]
        # Yine korelasyona göre en iyi 5 öneriyi buluyoruz
        top_recs = user_anime_pivot.corrwith(anime_name).sort_values(ascending=False).head(5)
        print(f"Top 5 recommendations for {animeBase}:")
        print(top_recs)
        for rec_title, corr_value in top_recs.items():
            if not registered_title_check(user_name, rec_title):
                if not Rec_title_check(user_name, rec_title):
                    prelist.append((rec_title, corr_value))
        return prelist
    else:
        print(f"{animeBase} not found in the pivot table.")

# Test fonksiyonu ile farklı animeleri kontrol edelim
recommendations = second_anime_Recs("Naruto", "emre")  # Burada önerilen animeleri istediğin gibi değiştirebilirsin
print(recommendations)
