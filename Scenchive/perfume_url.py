import requests
from bs4 import BeautifulSoup
import db_info # 모듈 import


# 쿼리 실행
mycursor = db_info.mydb.cursor()

mycursor.execute("SELECT brand_url FROM brand")
result = mycursor.fetchall()
result = [list(result[x]) for x in range(len(result))]

mycursor.execute("SELECT brand_name FROM brand")
result2 = mycursor.fetchall() # fetchall: 모든 검색 결과를 가져옴
result2 = [list(result2[x]) for x in range(len(result2))] # tuple -> list

for i in result:
    brand_url = i[0]
    print(brand_url)

    def get_perfumeurl():
        perfumelist_url = None

        # 1) perfume list 페이지 접근
        brandpage_url = "https://basenotes.com/" + brand_url
        html = requests.get(brandpage_url).text
        soup = BeautifulSoup(html, "html5lib")
        a_tag = soup.find("a", {"class": "otherperfumes"})
        
        if a_tag is not None:
            perfumelist_url = a_tag["href"]
            # print(perfumelist_url)
        else:
            print("No perfume-list url found.")

        # 2) perfume url 스크래핑
        if perfumelist_url is not None:
            url = "https://basenotes.com/" + perfumelist_url
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html5lib")

            for url_section in soup.find_all("div", class_="bncard card6"):
                perfume_url = url_section.find('a')["href"]
                print(perfume_url)

            # if brand_url_section is not None: # brand_url 변수가 None인 경우 출력하지 않음
            #     brand_url = brand_url_section.find('a')["href"]
            #     print(brand_url)
            #     sql = "UPDATE brand SET brand_url = %s WHERE brand_name = %s"
            #     val = (brand_url, brand)
            #     mycursor.execute(sql, val) # 테이블에 brand_url 삽입

    if brand_url is not None:
        perfumelist_url = get_perfumeurl()


# db_info.mydb.commit()