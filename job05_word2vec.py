# 형태소 갯수만급의 차원을 만든다, 주관은 어떻게 정해지냐?
# embedding 을 겪으면 의미적으로 비슷한 단어들 끼리 비슷한 좌표에 모이게 된다.=주관이 생긴다
# 1,2,3 등에 단어의 의미가 들어가 있어야 한다.
# 공간 상 배치를 하면 좌표가 생기고 백터로 사용가능
from gensim.models import Word2Vec
import pandas as pd

review_word = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')
review_word.info()

cleaned_token_review = list(review_word['cleaned_sentences']) # dataFrame의 cleaned_sentences만 리스트로
print(cleaned_token_review[0])
cleaned_tokens = []# 토큰 단위로 짜르기
for sentence in cleaned_token_review:
    token = sentence.split() # 디폴트 -> 띄어쓰기 token 단위로 짜르기
    cleaned_tokens.append(token)
print(cleaned_tokens[0]) # 토큰 단위로 짤라진 list

embedding_model = Word2Vec(cleaned_tokens, vector_size = 100, #vector_size-> 차원을 축소할 차원크기
                           window = 4, min_count=20, # window 몇개의 형태소로 해당하는 단어의 성질,
                           # 특징을 파악할 것인가? 형태소의 list에서 4개씩 짤라서 학습, conv의 kernel과 비슷,
                           # 일반적으로 4개 min_count->전체의 단어 중 사용의 빈도가 20번은 나와야 백터화
                           workers = 4, epochs = 100, sg = 1) #workers-> 컴퓨터 core(cpu) 갯수를 몇개 사용해야 하는가?, epochs 몇번 학습할 것인가
                            # sg 0->CBOW(back of word-> 단어가 , 1->Skip-gram 인배딩할 때의 알고리즘
# embedding_model, 빈도수가 20개 넘는 단어들의 100차원 좌표값
embedding_model.save('./models/word2vexModel.model')
print(embedding_model.wv.index_to_key)
print(len(embedding_model.wv.index_to_key))