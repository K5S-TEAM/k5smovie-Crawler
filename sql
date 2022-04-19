# SQL문 참고

# 데이터베이스 생성 
sql = "CREATE DATABASE k5smovie"

#  데이터베이스 목록 보기
sql = "show databases;"

# 테이블 생성문
sql = "CREATE TABLE mv_table ( code MEDIUMINT PRIMARY KEY, title VARCHAR(100), genre VARCHAR(100), nation VARCHAR(50), rating VARCHAR(100), score DOUBLE, director VARCHAR(100), "\
    + "actor VARCHAR(100), story VARCHAR(1500), opening_date VARCHAR(100), running_time VARCHAR(100), img VARCHAR(100) )" 

# # 테이블 목록 보기
sql = "show tables;"

# 테이블 삭제
sql = "DROP TABLE mv_table" 

# 테이블 구성 상태 살펴보기
sql = "DESCRIBE mv_table"

# 영화 정보 삽입
sql = "insert into mv_table values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# https://hotmovie.s3.ap-northeast-2.amazonaws.com/imgs/190695.png
path = "https://hotmovie.s3.ap-northeast-2.amazonaws.com/imgs/"
for i in range(len(real_list)):
	path2 = path + real_list[i][0] + ".png"
	vals = (real_list[i][0], real_list[i][1], real_list[i][2], real_list[i][3], real_list[i][4], real_list[i][5], real_list[i][6], real_list[i][7], real_list[i][8],  real_list[i][9],  real_list[i][10], path2)
	cur.execute(sql, vals)

# CODE로 테이블에 존재하는지 찾기
sql = "select * from mv_table where code = 190695"

# CODE로 테이블에서 삭제
sql = "delete from mv_table where code = 190695"

# 테이블에 몇개의 영화 정보가 있는지 확인
sql = "select count(*) from mv_table"