import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_2019_1_201.csv')
print(df.head())
df.info()

stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords_list = list(stopwords['stopword'])

cleaned_sentences = []
for review in df.reviews:
    review = re.sub('[^가-힇]', '', review)
    review_word = review.split(' ')
    words = []
    for word in review_word:
        if word not in stopwords_list:
            words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
df.info()
df.to_csv('./crawling_data/cleaned_review_2019_1_20.csv', index = False)
