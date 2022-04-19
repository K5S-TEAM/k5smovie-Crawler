import re
import os
from random import randrange
 
import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve
 
# 텍스트에 포함되어 있는 특수 문자 제거
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》 ]', '', readData)
    return text
 
# 청소년 관람 불가, 평점 없는 영화 제외
def crawling(start, finish):
    try:
        global ok
        ok = False
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["CODE", "TITLE", "GENRE", "NATION", "RATING", "SCORE", "DIRECTOR", "ACTOR", "STORY", "OPENING DATE", "RUNNING TIME"])
 
        success = 0
        
        for i in range(start, finish+1):
 
            movie_code = str(i)
            raw = requests.get("https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + movie_code)
            
            html = bs(raw.text, 'html.parser')

            # 컨테이너
            movie = html.select("div.article")

            # 영화관련 정보
            for a, m in enumerate(movie):
 
                # 제목
                title = m.select_one("h3.h_movie a")
                print(title.text)
                # 평점
                score = m.select_one("div.main_score div.score a div.star_score span.st_off span.st_on")
                
                # 평점 없으면 스킵
                non_score = "관람객 평점 없음"
                if (score == None) or (non_score in score.text) or ("0점" == score.text):
                    ok = False
                    continue
                
                # score에서 점수만 남기고 숫자로 변환
                score = score.text
                score = score[6:11]
                score = float(score)
                
                # 장르
                genre = m.select("dl.info_spec dd p span:nth-of-type(1) a")

                # 성인영화일 경우 스킵
                if "에로" in genre[0].text:
                        ok = False
                        continue

                # 국가
                nation = m.select_one("dl.info_spec dd p span:nth-of-type(2) a")
                
                # 감독
                directors = m.select("dl.info_spec dd:nth-of-type(2) p a")

                # 배우
                actors = m.select("dl.info_spec dd:nth-of-type(3) p a")
                
                # 배우 정보가 없을 경우 스킵 배우 정보쪽에 관람 등급이 적혀있는 경우도 스킵
                if len(actors) == 0:
                    continue
                else :
                    if "청소년 관람불가" in actors[0].text:
                        ok = False
                        continue
                    elif "15세 관람가" in actors[0].text:
                        ok = False
                        continue
                    elif "12세 관람가" in actors[0].text:
                        ok = False
                        continue
                    elif "전체 관람가" in actors[0].text:
                        ok = False
                        continue
                
                # 관람등급
                rating = m.select_one("dl.info_spec dd:nth-of-type(4) p a")
                
                # 줄거리
                story = m.select("div.story_area p.con_tx")
                
                # 개봉일
                opendate = m.select("dl.info_spec dd p span:nth-of-type(4):nth-child(n+3):nth-child(-n+4)")
                    
                # 상영시간
                runtime = m.select_one("dl.info_spec dd p span:nth-of-type(3)") 
                
                # 엑셀파일로 저장
                # TEXT로 리스트 만들기
                genre_list = [g.text for g in genre]
                directors_list = [d.text for d in directors]
                actors_list = [a.text for a in actors]
                story_list = [s.text for s in story]
                opendate_list = [op.text for op in opendate]
 
                # 필요한 데이터를 제대로 수집하지 못했을 경우 스킵
                if len(genre_list) == 0 or len(directors_list) == 0 or len(actors_list) == 0 or len(story_list) == 0 or len(opendate_list) == 0:
                    ok = False
                    continue
                
                # 여러개인 정보를 하나의 문자열로 만들기
                genre_str = ', '.join(genre_list)
                directors_str = ', '.join(directors_list)
                actors_str = ', '.join(actors_list)
                story_str = ', '.join(story_list)
                opendate_str = ', '.join(opendate_list)
 
                # 개봉일 공백 제거 후 다시 띄어쓰기
                opendate_str = re.sub('[\s]', '', opendate_str)
                opendate_str = re.sub(',', ', ', opendate_str)
                
                # 엑셀파일에 수집한 정보 삽입
                # sheet.append(["CODE", "TITLE", "GENRE", "NATION", "RATING", "SCORE", "DIRECTOR", "ACTOR", "STORY", "OPENING DATE", "RUNNING TIME"])
                sheet.append([movie_code, title.text, genre_str, nation.text, rating.text, score, directors_str, actors_str, story_str, opendate_str, runtime.text])

                # 포스터
                img_src = m.select_one("div.poster a img")
 
                # 다운로드
                path = '.\\imgs\\'
                mv_img_src = img_src.attrs["src"].split("?")
                urlretrieve(mv_img_src[0], path + movie_code + ".png")
                
                # 크롤링 모든 과정 완료
                ok = True

            # 크롤링 성공 갯수 확인    
            if ok == True:
                success = success + 1

            print(finish - i, " / ", finish - start)
            print(success, "개의 영화 정보저장 완료")
        
    except:
        print("에러발생")
        wb.save("k5smovie.xlsx")
    finally:
        print("완료")
        wb.save("k5smovie.xlsx")

if __name__ == "__main__":
    # 네이버 영화 코드 번호를 이용해 크롤링 시작과 끝 코드번호를 넣어주면 작동
    crawling(190695, 195000)