import pandas as pd
import glob
data_paths = glob.glob('./crawling_data/datasets/*') # 경로 가져오기
print(data_paths)
df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.columns = ['title', 'cleaned_sentences'] # col이 맞지 않는 것들을 같은 col로 통일
    df = pd.concat([df, df_temp], ignore_index=True,
              axis='rows')
df.info()
df.to_csv('./crawling_data/datasets/movie_review_2018_2020.csv',
          index=False)

