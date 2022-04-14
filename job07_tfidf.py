import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread # 행열 저장, 읽을 때 사용
import pickle
# Tf 문장 빈도, Df 문장 전체에서의 빈도-> 한문장에서의 빈도는 유사도 up, 전체 문장에서의 빈도는 유사도를 찾는데 도움 X, I-> 역수곱
# 단순 곱은 아니고 따로 식이 존재
df_reviews = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')
df_reviews.info()
df_reviews.dropna(inplace = True)
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['cleaned_sentences']) #Tfidf형태로 fit_transform, 문장별로 유사도를 측정한 행열

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)
mmwrite('./models/tfidf_movie_review.mtx', Tfidf_matrix)
