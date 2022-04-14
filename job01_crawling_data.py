# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022

from selenium import webdriver
import pandas as pd
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')  이거 활성화하면 웹 브라우저가 안 뜸. 보고싶으면 주석 풀면 되고. 근데지금은 주석하래. 지금은 이거 하면 에러뜬대

options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')   #이 아래 3개는 맥 어쩌고에서 필요한 거임. 윈도우 주석 풀어놔도 괜찮음.
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')

driver= webdriver.Chrome('./chromedriver', options = options)
driver.implicitly_wait(1) # 로딩이 빨리 되면 바로 읽어오고, 안 되면 1초 기다리기
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1 첫 페이지
# //*[@id="old_content"]/ul/li[1]/a 영화제목 1
# //*[@id="old_content"]/ul/li[2]/a 영화제목 2
# //*[@id="old_content"]/ul/li[20]/a 영화제목 20

# //*[@id="old_content"]/div[3]/table/tbody/tr/td[1] 영화 페이지 버튼

# https://movie.naver.com/movie/bi/mi/review.naver?code=193794&page=2  리뷰 페이지 url

# //*[@id="movieEndTabMenu"]/li[6]/a/em 리뷰버튼
# //*[@id="movieEndTabMenu"]/li[4]/a/em

# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰제목 1
# //*[@id="reviewTab"]/div/div/ul/li[2]/a/strong 리뷰제목 2

# //*[@id="content"]/div[1]/div[2]/div[1]/h3/a 영화 제목
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4] 리뷰
movie_page_url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2019&page={}'
movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'
review_page_url = 'https://movie.naver.com/movie/bi/mi/review.naver?code=193794&page={}'
review_tab_xpath = '//*[@id="movieEndTabMenu"]/li[{}]/a'
review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'
title_xpath = '//*[@id="content"]/div[1]/div[2]/div[1]/h3/a'
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'

title_list = []
review_list = []
for i in range(5, 21):
    url = movie_page_url.format(i) # 영화 페이지
    for j in range(1, 21):
        try:
            try:
                driver.quit()
            except:
                pass
            driver = webdriver.Chrome('./chromedriver', options=options)
            driver.implicitly_wait(1)
            print(url)
            driver.get(url)
            print('debug10')
            time.sleep(0.2)
            try:
                print('j :', j)
                driver.find_element_by_xpath(movie_title_xpath.format(j)).click() # 영화 제목 클릭
                time.sleep(0.2)
                for k in range(6, 0, -1):
                    if driver.find_element_by_xpath(review_tab_xpath.format(k)).text == '리뷰':
                        print(review_tab_xpath.format(k))
                        review_page_url = driver.find_element_by_xpath(review_tab_xpath.format(k)).get_attribute('href')
                        print(review_page_url)
                        driver.find_element_by_xpath(review_tab_xpath.format(k)).click() # 리뷰 버튼 클릭
                        time.sleep(0.2)

                        break

                for l in range(1, 7):
                    print('l :', l)
                    try:
                        print(review_page_url)
                        #driver.get(review_page_url + '&page={}'.format(l))
                        driver.find_element_by_xpath('//*[@id="pagerTagAnchor{}"]'.format(l)).click()
                        print('debug02')
                        time.sleep(0.2)
                        for k in range(1, 11):
                            try:
                                driver.find_element_by_xpath(review_title_xpath.format(k)).click() # 리뷰 제목 클릭
                                time.sleep(0.2)
                                print('k :', k)
                                try:
                                    title = driver.find_element_by_xpath(title_xpath).text
                                    title = title.replace(',', ' ')
                                    review = driver.find_element_by_xpath(review_xpath).text
                                    review = review.replace(',', ' ')
                                    title_list.append(title)
                                    review_list.append(review)
                                    try:
                                        driver.back()  # 리뷰 페이지로
                                        time.sleep(0.2)
                                    except:
                                        driver.get(review_page_url.format(l))
                                        time.sleep(0.2)
                                except:
                                    try:
                                        driver.back()  # 리뷰 페이지로
                                        time.sleep(0.2)
                                    except:
                                        driver.get(review_page_url.format(l))
                                        time.sleep(0.2)

                            except:
                                print('{}페이지 {}번째 영화 리뷰 {}페이지 {}번째 리뷰 error'.format(i, j, l, k))
                                driver.back()
                                continue
                    except:
                        print('{}페이지 {}번째 영화 리뷰 {}페이지 error'.format(i, j, l))
                        #driver.get(url)
                        break
            except:
                print('{}페이지 {}번째 영화 error'.format(i, j))
        except:
            print('{}page error'.format(i))
    df = pd.DataFrame({'title':title_list, 'reviews':review_list})
    print(df.tail())
    df.to_csv('./crawling_data/reviews_{}_1_20.csv'.format(2019), index=False)
driver.close()
