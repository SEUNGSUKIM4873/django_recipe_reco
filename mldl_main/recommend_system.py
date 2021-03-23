from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings

import pandas as pd

def recommend_recipe_list(ingredients_list) :
    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    df = pd.read_excel( settings.MEDIA_ROOT_URL + settings.MEDIA_URL + 'recipe_DB.xlsx')
    # df_save_ingredient =  pd.read_excel(base_url + 'save_ingredient_DB.xlsx', index_col = 0)

    similarity_list = list()
    doc1 = ''
    for ingredient in ingredients_list :
        doc1 += ' ' + ingredient

    for index,recipe_ingre in enumerate(df['Ingredient']) :
        doc2 = recipe_ingre
        corpus = [doc1, doc2]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus).todense()
        similarity = cosine_similarity(X[0], X[1])

        similarity_list.append(similarity)

    df_recommend = df.copy()
    df_recommend['Similarity'] = similarity_list

    # 유사도 float type 변환
    df_recommend['Similarity'] =  df_recommend['Similarity'].astype(float)

    # 추천 지수 생성
    df_recommend['Reco_index'] = (df_recommend['Time(minute)']*-0.0000004) + (df_recommend['Scrap']*0.0000002) + (df_recommend['Judge']* 0.002) + df_recommend['Similarity']


    time_list = list()
    for time in df_recommend['Time(minute)']:
        time_list.append(str(time) + '분')
    df_recommend['Time(minute)'] = time_list

    df_recommend.sort_values('Reco_index',ascending=False, inplace=True)
    df_recommend_now = df_recommend[['Title','Time(minute)','Ingredient','URL']].reset_index(drop=True).head(10)


    return df_recommend_now
