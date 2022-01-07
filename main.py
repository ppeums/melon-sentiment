from melon import melon, get_singer
from pos import makePos
import time

# 장르명 => BALAD, DANCE, RAP, RB, INDIE, ROCK, TROT, FORK

genre = 'BALAD'
start = 29  # 실제 페이지 = start+1
end = 30

start_time = time.time()    # 시간 측정 시작

# 노래 크롤링
for page in range(start, end):  # 설정한 페이지만큼 노래 크롤링
    print(f"========== Scrapping {genre}: Page {page+1} ==========")
    melon(genre, page)

# 감성분석
makePos(genre)

# 가수인기도 크롤링
get_singer()

print('--- %s seconds ---' % (time.time() - start_time))    # 실행 시간 출력
