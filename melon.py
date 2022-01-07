from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import islice
import re
import time
import random
import csv

options = webdriver.ChromeOptions()
options.add_argument('headless')

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
}

LYRIC_URL = "https://www.melon.com/song/detail.htm?songId="         # 곡 정보 페이지 URL
SINGER_URL = "https://www.melon.com/artist/timeline.htm?artistId="  # 가수 정보 페이지 URL

# 가수인기도 크롤링
def get_singer():
    rfile = open(f'first_singer.csv', mode='r', buffering=-1, encoding='utf-8')
    wfile = open(f'first_singer_like.csv', mode='a', buffering=-1, encoding='utf-8', newline='')
    reader = csv.reader(rfile)
    writer = csv.writer(wfile)

    start = 1200
    end = 2064

    for line in islice(reader, start, end):
        singer_id = line[0]
        print(f'CNT {start}')

        driver = webdriver.Chrome('C:/Users/user/PycharmProjects/chromedriver', chrome_options=options)
        driver.implicitly_wait(3)   # 딜레이 주기
        driver.get(f'{SINGER_URL}{singer_id}')  # 가수 정보 페이지 가져오기

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        singer_like = soup.select('.wrap_intst .fan_area .cnt_fan_b .no')[0].text   # 가수인기도 가져오기
        singer_like = int(singer_like.replace(',', ''))

        newline = {'singer_id': singer_id, 'singer_like': singer_like}
        print(f'ID {singer_id}: like {singer_like}')
        start += 1
        writer.writerow(list(newline.values()))

# 장르별 크롤링
def melon(genre, page):
    url = get_url(genre)
    driver = webdriver.Chrome('C:/Users/user/PycharmProjects/chromedriver', chrome_options=options)
    driver.implicitly_wait(3)   # 딜레이 주기
    driver.get(f'{url}&startIndex={page*50+1}')     # 페이지 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll("div", {"class": "wrap_song_info"})
    start = page*50+1

    for result in results:
        print(f'{genre} {start}')

        if result.find("div", {"class": "ellipsis rank03"}):
          continue
        rand_value = random.uniform(2, 4)   # 랜덤 딜레이 주기
        time.sleep(rand_value)

        gname = genre.lower()
        file = open(f"first_{gname}_1451.csv", mode="a", buffering=-1, encoding='utf-8', newline='')
        writer = csv.writer(file)
        writer.writerow(["id", "date", "like", "lyric", "singer_id"])   # 속성 row 추가

        song_id = result.find("div", {"class": "ellipsis rank01"})  # 노래ID 가져오기
        song_id = result.find("a")["href"]
        song_id = re.findall("\d+", song_id)
        song_id = song_id[1]

        rand_value = random.uniform(2, 4)   # 랜덤 딜레이 주기
        time.sleep(rand_value)
        driver.get(f'{LYRIC_URL}{song_id}')  # 곡 정보 페이지 가져오기

        dhtml = driver.page_source
        dsoup = BeautifulSoup(dhtml, 'html.parser')
        singer_id = dsoup.select('.section_info .artist a')[0]['href']  # 가수ID 가져오기
        singer_id = singer_id.split("'")[1]

        date = driver.find_element_by_class_name('list').text   # 발매일 가져오기
        date = date.split('\n')[3].replace('.', '')

        like = driver.find_element_by_id('d_like_count').text   # 노래 좋아요 수 가져오기
        like = int(re.sub(',', '', like))
        print(f'{genre} {start}: like {like}')

        try:    # 가사 가져오기
            lyric = driver.find_element_by_class_name('lyric').text
            lyric = lyric.replace('"', '')
        except:    # 가사가 없을 경우 예외 처리
            lyric = ''

        newline = {'id': song_id, 'date': date, 'like': like, 'lyric': lyric, 'singer_id': singer_id}
        writer.writerow(list(newline.values()))
        start += 1

# 장르별 URL 가져오기
def get_url(genre):
    if genre == 'BALAD':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0100#params%5BgnrCode%5D=GN0100&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'DANCE':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0200#params%5BgnrCode%5D=GN0200&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'RAP':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0300#params%5BgnrCode%5D=GN0300&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'RB':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0400#params%5BgnrCode%5D=GN0400&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'INDIE':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0500#params%5BgnrCode%5D=GN0500&params%5BdtlGnrCode%5D=GN0501&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'ROCK':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0600#params%5BgnrCode%5D=GN0600&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'TROT':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0700#params%5BgnrCode%5D=GN0700&params%5BdtlGnrCode%5D=GN0701&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    elif genre == 'FORK':
        URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0800#params%5BgnrCode%5D=GN0800&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj'
    return URL
