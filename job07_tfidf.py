import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread # 행열 저장, 읽을 때 사용
import pickle

df_reviews = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')
df_reviews.info()
df_reviews.dropna(inplace = True)
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['cleaned_sentences']) #Tfidf형태로 fit_transform, 문장별로 유사도를 측정한 행열

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)
mmwrite('./models/tfidf_movie_review.mtx', Tfidf_matrix)
