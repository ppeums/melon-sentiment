from konlpy.tag import Mecab
from itertools import islice
import csv

def makePos(genre):
    mecab = Mecab()
    genre = genre.lower()
    rfile = open(f'first_{genre}_1-50.csv', mode='r', buffering=-1, encoding='utf-8')
    wfile = open(f'first_{genre}_senti.csv', mode='a', buffering=-1, encoding='utf-8', newline='')
    reader = csv.reader(rfile)
    writer = csv.writer(wfile)
    writer.writerow(['id', 'date', 'like', 'senti', 'singer_id'])   # 속성 row 추가

    pos_cnt = 0
    neg_cnt = 0
    neu_cnt = 0
    none_cnt = 0

    start = 0
    end = 50

    for line in islice(reader, start, end):  # song_genre.csv의 row 1개 = 노래 1개
        try:
            if line[3] == 'lyric':
                continue
        except:
            continue

        id = line[0]        # 노래ID
        date = line[1]      # 발매일
        like = line[2]      # 좋아요 수
        pos = mecab.pos(line[3])    # 가사 형태소 분석
        singer_id = line[4]         # 가수ID

        positive = 0        # 긍정점수
        negative = 0        # 부정점수
        neutral = 0         # 중립점수

        for item in pos:    # 노래 1개의 형태소 1개
            newitem = item[0] + '/' + item[1]   # 형태소 형식 재구성

            pfile = open('polarity.csv', mode='r', buffering=-1, encoding='utf-8')
            preader = csv.reader(pfile)

            for pline in preader:   # 감성사전의 row 1개
                if pline[0] == newitem:     # 감성 데이터 분석
                    senti = pline[7]
                    if senti == 'POS':
                        positive += 1
                    elif senti == 'NEG':
                        negative += 1
                    elif senti == 'NEUT':
                        neutral += 1
                    continue

        if positive == 0 and negative == 0 and neutral == 0:    # 가사가 없을 경우
            senti = 'None'
            none_cnt += 1
        else:
            if positive == negative:
                senti = 'NEUT'
                neu_cnt += 1
            else:
                if positive > negative:
                    senti = 'POS'
                    pos_cnt += 1
                else:
                    senti = 'NEG'
                    neg_cnt += 1

        newline = {'id': id, 'date': date, 'like': like, 'senti': senti, 'singer_id': singer_id}
        print(f'Sentiment {genre.upper()}: CNT {start+1}')
        start += 1
        writer.writerow(list(newline.values()))
