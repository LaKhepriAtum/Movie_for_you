import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

form_window = uic.loadUiType('./mainWidget.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_reviews = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')
        self.Tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)  # model 가져오기
        self.titles = list(self.df_reviews['title']) # DataFrame의 title을 list화
        self.titles.sort() # 정렬하기
        for title in self.titles:
            self.cmb_titles.addItem(title) #cmb에 titles 모두 집어 넣기
            
        model = QStringListModel()
        model.setStringList(self.titles) # list 된 title 을 자동완성 되도록
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)
        
        self.cmb_titles.currentIndexChanged.connect( # cmb_titles의 index가 달라졌을 때
            self.cmb_titles_slot) # cmb_titles_slot함수 호출
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)

    def btn_recommend_slot(self):
        sentence = self.le_keyword.text()
        if sentence not in self.titles: # title 안에 sentence이 있다고 한다
            input_words = sentence.split()
            if len(input_words) < 10:
                key_word = input_words[0]# 여러 단어를 적었을 경우, 첫 번째 만 사용
                embedding_model = Word2Vec.load('./models/word2vexModel.model')
                try: # 모르는 단어를 적었을 경우
                    sim_word = embedding_model.wv.most_similar(key_word, topn=10) # key_word와 가장 큰 유사도를 보여주는 10개 가져오기(주관)
                except:
                    return self.lbl_recommend.setText('제가 모르는 단어예요 ㅜㅜ')
                sentence = [key_word] * 11
                words = []
                for word, _ in sim_word:
                    words.append(word)
                for i, word in enumerate(words):
                    sentence += [word] * (10 - i) # 유사도가 큰 순서대로 가중치를 부여(10 - i 번 반복하도록)
                sentence = ' '.join(sentence)
        recommendation_titles = self.recommend_by_sentence(sentence)
        self.lbl_recommend.setText(recommendation_titles)

    def cmb_titles_slot(self):
        title = self.cmb_titles.currentText()# 영화 제목 가져오기cmb의 현재 index
        recommendation_titles = self.recommend_by_movie_title(title) #recommend_by_movie_title 함수에 title 주기
        self.lbl_recommend.setText(recommendation_titles)

    def recommend_by_sentence(self, sentence):
        sentence_vec = self.Tfidf.transform([sentence]) # pickle 에 맞게 transform
        cosin_sim = linear_kernel(sentence_vec, self.Tfidf_matrix) #sentence_vec 와 Tfidf_matrix 비교 코사인 값을 리턴
        recommendation_title = self.getRecommendation(cosin_sim) # 함수 돌리고
        recommendation_title = '\n\n'.join(recommendation_title) #\n\n 으로 합치기
        return recommendation_title

    def recommend_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['title']==title].index[0] # 인자와 같은 title 의 행 정보 가져오기
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], # 내가 고른 하나의 문장
                                   self.Tfidf_matrix) # 내가 고른 하나의 문장과 전체 10 문장에 대한 cos 유사도를 return
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n\n'.join(list(recommendation_titles))
        return recommendation_titles

    def getRecommendation(self, cosine_sim): # class 안에서 함수 만들 경우 첫 번째 변수는 self
        simScore = list(enumerate(cosine_sim[-1]))  # 2중 리스트 풀기, enumerate->index 값을 준다
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 1번 index 기준으로 sort,  reverse=True(내림차순)
        simScore = simScore[1:11]  # 유사한 것 10개, [0]은 자기자신 코사인 유사도가 가장 큰 10개
        movieidx = [i[0] for i in simScore]  # 가장 유사한 영화의 'enumerate->index 값을 준다'의 index 를 리스트로
        recMovieList = self.df_reviews.iloc[movieidx]  # index 를 리스트로의 행
        return recMovieList.iloc[:, 0]  # 모든 행의 0번째(title)




app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())