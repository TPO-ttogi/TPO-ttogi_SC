import mysql.connector
import requests
from bs4 import BeautifulSoup

# MySQL 서버와 연결 -> !! 깃헙 push 전 암호화 필수 !!
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="0128",
  database="scenchive"
)

# 쿼리 실행
mycursor = mydb.cursor()
mycursor.execute("SELECT brand_name FROM brand")
result = mycursor.fetchall() # fetchall: 모든 검색 결과를 가져옴
result = [list(result[x]) for x in range(len(result))] # tuple -> list


for i in result:
    brand = i[0]
    brand_name = i[0].replace(" ", "+") # basenotes의 url 형식에 적합한 형태로 변환

    def get_brand_url():
        url = "https://basenotes.com/brands/?q=" + brand_name
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html5lib")
        brand_url_section = soup.find('div', class_="bncard card6")
        if brand_url_section is not None: # brand_url 변수가 None인 경우 출력하지 않음
            brand_url = brand_url_section.find('a')["href"]
            print(brand_url)
            sql = "UPDATE brand SET brand_url = %s WHERE brand_name = %s"
            val = (brand_url, brand)
            mycursor.execute(sql, val) # 테이블에 brand_url 삽입

    get_brand_url()

# mydb.commit() # 데이터 변경 결과 db에 반영

  