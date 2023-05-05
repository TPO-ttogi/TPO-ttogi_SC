import requests
from bs4 import BeautifulSoup
import db_info # 모듈 import


# 쿼리 실행
mycursor = db_info.mydb.cursor()

mycursor.execute("SELECT * FROM brand")
result = mycursor.fetchall() # fetchall: 모든 검색 결과를 가져옴
result = [list(result[x]) for x in range(len(result))] # tuple -> list

for i in result:
    brand_id = i[0]
    brand_url = i[2]
    print(brand_url)

    def get_perfumelist():
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

        # 2) perfume list 스크래핑
        if perfumelist_url is not None:
            url = "https://basenotes.com/" + perfumelist_url
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html5lib")
            
            # TODO: perfume_image scraping
            for perfume_name in soup.find_all("span", class_="cardname"):
                print(perfume_name.text)
                sql = "INSERT INTO perfume (perfume_name) VALUES (%s)"
                val = (perfume_name.text,)
                mycursor.execute(sql, val)

                sql = "UPDATE perfume SET brand_id = %s WHERE perfume_name = %s"
                val = (brand_id, perfume_name.text)
                mycursor.execute(sql, val)


    if brand_url is not None:
        perfumelist_url = get_perfumelist()


db_info.mydb.commit()