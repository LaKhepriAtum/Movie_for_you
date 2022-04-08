import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec

df_reviews = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1])) #2중 리스트 풀기, enumerate->index 값을 준다
    simScore = sorted(simScore, key = lambda x:x[1], reverse=True) #1번 index 기준으로 sort,  reverse=True(내림차순)
    simScore = simScore[1:11] # 유사한 것 10개, [0]은 자기자신 코사인 유사도가 가장 큰 10개
    movieidx = [i[0] for i in simScore] # 가장 유사한 영화의 'enumerate->index 값을 준다'의 index 를 리스트로
    recMovieList = df_reviews.iloc[movieidx]# index 를 리스트로의 행
    return recMovieList.iloc[:, 0] # 모든 행의 0번째(title)

Tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr() # matrix 가져오기
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f) # model 가져오기

# 영화 제목 이용
# movie_idx = df_reviews[df_reviews['title'] =='어벤져스: 엔드게임'].index[0] #df_reviews['title'] =='기생충'조건 .index[0]->title, .index[1]-> cleaned_sentences
# print(movie_idx)

#영화 index이용
# movie_idx = 218
# print(df_reviews.iloc[movie_idx, 0]) # movie_idx 조건의 o 번째 col df.iloc[행, 열]
# cos 가 1에 가깝다 = 유사한 문장이다. , -1에 가깝다 = 반대다, 0에 가깝다 = 유사성X
#
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix) # 1에 가까우면 유사하다.Tfidf_matrix[movie_idx]관심영화 ,  Tfidf_matrix나머지 모든 영화
#의 cosine 유사도를 준다, len->Tfidf_matrix의 갯수, 2중 리스트
# print(cosine_sim)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# key_word 이용
# embedding_model = Word2Vec.load('./models/word2vexModel.model')
# key_word = ''
# sim_word = embedding_model.wv.most_similar(key_word, topn=10) # key_word와 가장 큰 유사도를 보여주는 10개 가져오기
# sentence = [key_word] * 11
# words = []
# for word, _ in sim_word:
#     words.append(word)
# for i, word in enumerate(words):
#     sentence += [word] * (10 - i) # 유사도가 큰 순서대로 가중치를 부여
#
# sentence = ' '.join(sentence)
sentence = '적화통일돼서 배에서 기생충 키우고 싶나? 뭔 북한넘들 미화 영화가 이렇게 많냐.배우들도 생각이 있으면 이런 영화는 걸러야하는 거 아니냐.박정희, 전두환 군부 독재 시절을 미화하는 영화에 출연하면 무식해보이 듯이,이런 북한 미화 영화 출연하는 것도 참으로 정신나간 듯이 보인다.제목도 강철비가 뭐냐. 김영환 강철서신에서 가져온거냐.정말 적당히 하자.'
sentence_vec = Tfidf.transform([sentence]) #pickle 로 백터값 만들기
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix) # 백터값들과 영화의 백서값으로 새로운 유사도 찾기

# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)

