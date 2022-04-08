import pandas as pd
df1 = pd.read_csv('./crawling_data/reviews_2021_1_3.csv')
df2 = pd.read_csv('./crawling_data/reviews_2021_4_20.csv')

df = pd.concat([df1, df2], ignore_index=True, axis='rows')
df.to_csv('./crawling_data/reviews_2021_1_20.csv', index = False)