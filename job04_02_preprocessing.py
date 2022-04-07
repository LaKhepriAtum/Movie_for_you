import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/cleaned_review_2019_1_20.csv')
df.dropna(inplace=True)
print(df.head())
df.info()
print(df.isnull().sum())

okt = Okt()
count = 0
cleaned_sentences = []
for sentence in df.cleaned_sentences:
    count += 1
    if count % 10 ==0:
        print('.', end='')
    if count % 100 == 0:
        print()
    token = okt.pos(sentence, stem=True)
    # print(token)
    df_token = pd.DataFrame(token,  columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                                (df_token['class']=='Verb') |
                                (df_token['class']=='Adjective')]
    cleaned_sentence = ' '.join(df_token.word)
    # print(cleaned_sentence)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df.info()
df.to_csv('./crawling_data/cleaned_review_2019_20.csv', index = False)