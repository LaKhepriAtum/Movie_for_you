import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_review_2021_20.csv')
df.dropna(inplace=True) # null 값 제거
print(df.head())
df.info()
print(df.head())
print(df.duplicated().sum())
df.drop_duplicates(inplace= True) # 중복 제거
df.info()

one_sentences = []
for title in df['title'].unique():
    temp = df[df['title'] == title] # title이 같은 거 찾기
    temp = temp['cleaned_sentences']
    one_sentence = ' '.join(temp) # 하나의 문장으로 합친다.
    one_sentences.append(one_sentence)
df_one_sentence = pd.DataFrame(
    {'titles':df['title'].unique(), 'cleaned_sentences':one_sentences})
print(df_one_sentence.head())

df_one_sentence.to_csv('./crawling_data/movie_review_onesentence_2021_1_20.csv', index = False)