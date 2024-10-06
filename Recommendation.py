import pandas as pd
import sys 
sys.path.append("C:/Users/emref/Desktop/C13digihome/REcs_of_D")
from Recs_of_D import Rec_title_check,registered_title_check

user_anime_df = pd.read_csv("C:\Users\emref\Desktop\processed_data2.csv")
#print(user_anime_df.columns)
user_anime_pivot = user_anime_df.pivot_table(index=["user_id"], columns=["Title"], values="user_score")
user_anime_pivot = user_anime_pivot.fillna(user_anime_pivot.mean())
#print(user_anime_pivot.tail())

def anime_Recs(animeBase,user_name):
    #from Recs_of_D import Rec_title_check,registered_title_check
    prelist = []
    if animeBase in user_anime_pivot:
        anime_name = user_anime_pivot[animeBase]
        # taking the recommendations for the specific anime
        top_recs = user_anime_pivot.corrwith(anime_name).sort_values(ascending=False).head(5)
        print(top_recs)
        for rec_title, corr_value in top_recs.items():# Iterate over the titles, not the correlation values
            # Ensure you are checking the recommendation titles, not the base anime
            if not registered_title_check(user_name, rec_title):
                if not Rec_title_check(user_name, rec_title):
                    prelist.append((rec_title, corr_value))
        return prelist
        #print(prelist)
    else:
        print(f"{animeBase} not found in the pivot table.")
#anime_Recs("Bakemonogatari")

