# crawling 작업

# crawling은 각자 진행 하고 빨리 완성되는 코드로 연도를 나눠서 진행하겠습니다.
# 일단 2022년 개봉작만 진행해 주시고 저장형식은 csv로 하겠습니다.
# 나머지는 연도별로 나눠서 작업하고 합칠게요.
# 컬럼명은 ['title', 'reviews']로 통일해주세요.
# index=False 옵션으로 인덱스 없이 저장해주세요.
# 파일명은 "reviews_{}.csv".format(연도)로 해주세요.
# 크롤링한 데이터 파일은 아래 링크로 올려주세요.
# https://drive.google.com/drive/folders/1NLkgk0zSJlmNwSGq-q1qf6oBUZZLN9AK?usp=sharing

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import sys
import io


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}

total_page = 1
movies_no = []
for i  in range(total_page) :
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page={}'.format(i)

    res = requests.get(url, headers=headers)
    html = res.content.decode('utf-8', 'replace')
    res.raise_for_status()
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find("ul",{"class":"directory_list"})

    for content in contents.find_all("li"):
        if 'code' in (content.find("a")["href"]) :
            movie_no = re.sub(r'[^0-9]', '', (content.find("a")["href"]))
            movies_no.append(int(movie_no))
# print(type(movies_no[0]))
# print(movies_no[0])

url_list = []

for i in range(len(movies_no)) :
    reviews_no = []
    is_end = False
    for review_page in range(1, 7):
        if is_end:
            break
        url= 'https://movie.naver.com/movie/bi/mi/review.naver?code={}&page={}'.format(movies_no[i],review_page)
        res = requests.get(url, headers=headers)
        html = res.content.decode('utf-8', 'replace')
        res.raise_for_status()
        soup = BeautifulSoup(html, 'html.parser')
        con = soup.find("ul", {"class": "rvw_list_area"})
        try:
            for content in con.find_all("li"):

                review_no = re.sub(r'[^0-9]', '', (content.find("a")["onclick"]))
                if review_no in reviews_no:
                    is_end = True
                    break
                reviews_no.append(int(review_no))

        except:
            continue
    # print(reviews_no)
    url_list.append([movies_no[i], reviews_no])
# print(url_list)
df = pd.DataFrame()
titles = []
review = []
for url_movie in url_list:
    for url_review in url_movie[1]:
        url = 'https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={}&code={}&order=#tab'.format(url_review, url_movie[0])
        res = requests.get(url, headers=headers)
        html = res.content.decode('utf-8', 'replace')
        res.raise_for_status()
        soup = BeautifulSoup(html, 'html.parser')
        p_title = soup.find("h3", {"class": "h_movie"})
        p = p_title.find("a").get_text()
        p_review = soup.find("div", {"class": "user_tx_area"}).get_text()

        titles.append(p)
        review.append(p_review)
# print(titles)
# print(review)

df = pd.DataFrame({'title':titles, 'reviews':review})

print(df.head())
df.to_csv('./reviews_{}.csv'.format(2022), encoding='utf-8-sig', index=False, errors='ignore')

