import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}


options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")
driver= webdriver.Chrome('./chromedriver', options = options)

time.sleep(0.1)
title_list = []
reviews_list = []

for i in range(1,2):
    url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page={i}'
    driver.get(url)
    for j in range(1,3): #
        try:
            driver.find_element_by_xpath(f'//*[@id="old_content"]/ul/li[{j}]/a').click()
        except NoSuchElementException:
            print('NoSuchElementException1')
        url1 = driver.current_url[-6:]
        for l in range(1,4):
            url1 = f'https://movie.naver.com/movie/bi/mi/review.naver?code={url1}&page={l}'
            driver.get(url1)
            for k in range(1, 10):
                try:
                    driver.find_element_by_xpath(f'//*[@id="reviewTab"]/div/div/ul/li[{k}]/a').click()
                except NoSuchElementException:
                    print('NoSuchElementException2')
                # resp = requests.get(url, headers=headers)
                # soup = BeautifulSoup(resp.text, 'html.parser')
                # title = soup.select('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')
                time.sleep(0.1)
                try:
                    reviews = driver.find_element_by_css_selector('#content > div.article > div.obj_section.noline.center_obj > div.review > div.user_tx_area').text
                    reviews = re.compile('[^가-힣a-zA-Z ]').sub(' ', reviews)
                    title = driver.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
                    title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)
                    reviews_list.append(reviews)
                    title_list.append(title)
                    driver.back()
                except NoSuchElementException:
                    print('NoSuchElementException3')
                print(k)
        driver.get(url)
        time.sleep(0.1)
print(title_list)
print(reviews_list)
        #
        # driver.find_element_by_xpath(f'//*[@id="movieEndTabMenu"]/li[6]/a/em').click()
        # for k in range():
        # title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a').text
        # reviews = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
        # print(title)
# except:
#     print('error')

