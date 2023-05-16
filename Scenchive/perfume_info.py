import requests
from bs4 import BeautifulSoup
import db_info
import googletrans


# 쿼리 실행
mycursor = db_info.mydb.cursor()
mycursor.execute("SELECT brand_url FROM brand WHERE id >= 291 && id <= 297")
result = mycursor.fetchall() # fetchall: 모든 brand_url 검색 결과를 가져옴
result = [list(result[x]) for x in range(len(result))] # tuple -> list

# 번역 객체 생성
translator = googletrans.Translator()

j = 7909

for i in result:
    brand_url = i[0]
    print(brand_url)

    # perfume 상세 페이지 URL을 스크래핑하는 함수
    def get_perfumeurl():
        perfumelist_url = None
        perfume_urls = [] # 추가한 코드

        # 1) perfume list 페이지 접근
        brandpage_url = "https://basenotes.com" + brand_url
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
                perfume_urls.append(perfume_url)
                
            return perfume_urls # 추가한 코드


    # perfume 노트 정보와 이미지 스크래핑하는 함수
    # TODO: pefume 이미지 스크래핑

    def get_perfumeinfo(perfume_urls):
        global j

        for url in perfume_urls:

            url = "https://basenotes.com" + url
            print(url)
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html5lib")
            ol_tag = soup.find("ol", {"class": "fragrancenotes"})

            top_notes = []
            middle_notes = []
            base_notes = []

            h3_exists = False

            if ol_tag is not None:
                for h3 in ol_tag.find_all('h3'):
                    h3_exists = True
                    if h3.string.strip() == 'Top Notes': # top 노트 스크래핑
                        ul = h3.find_next_sibling('ul')
                        if ul:
                            for note in h3.find_next_sibling('ul').find_all('a'):
                                top_note = note.string.strip()

                                if top_note == "ylang" and "ylang ylang" not in top_notes:
                                    top_note = "ylang ylang"

                                top_note_kr = translator.translate(top_note, dest='ko').text

                                if top_note not in top_notes and top_note != "ylang":
                                    top_notes.append(top_note)
                                    sql = "INSERT INTO perfumescent (perfume_id, note_id, scent, scent_kr) VALUES (%s, %s, %s, %s)"
                                    val = (j, 1, top_note, top_note_kr)
                                    # print(val)
                                    mycursor.execute(sql, val)

                    elif h3.string.strip() == 'Middle Notes' or h3.string.strip() == 'Heart Notes': # middle(heart) 노트 스크래핑
                        ul = h3.find_next_sibling('ul')
                        if ul:
                            for note in h3.find_next_sibling('ul').find_all('a'):
                                middle_note = note.string.strip()
                                
                                if middle_note == "ylang" and "ylang ylang" not in middle_notes:
                                    middle_note = "ylang ylang"

                                middle_note_kr = translator.translate(middle_note, dest='ko').text

                                if middle_note not in middle_notes and middle_note != "ylang":
                                    middle_notes.append(middle_note)
                                    sql = "INSERT INTO perfumescent (perfume_id, note_id, scent, scent_kr) VALUES (%s, %s, %s, %s)"
                                    val = (j, 2, middle_note, middle_note_kr)
                                    # print(val)
                                    mycursor.execute(sql, val)

                    elif h3.string.strip() == 'Base Notes': # base 노트 스크래핑
                        ul = h3.find_next_sibling('ul')
                        if ul:
                            for note in h3.find_next_sibling('ul').find_all('a'):
                                base_note = note.string.strip()

                                if base_note == "ylang" and "ylang ylang" not in base_notes:
                                    base_note = "ylang ylang"

                                base_note_kr = translator.translate(base_note, dest='ko').text

                                if base_note not in base_notes and base_note != "ylang":
                                    base_notes.append(base_note)
                                    sql = "INSERT INTO perfumescent (perfume_id, note_id, scent, scent_kr) VALUES (%s, %s, %s, %s)"
                                    val = (j, 3, base_note, base_note_kr)
                                    # print(val)
                                    mycursor.execute(sql, val)

                            j += 1

                if not h3_exists: # h3 태그가 없는 경우
                    for a in ol_tag.find_all('a'):
                        top_note = a.string.strip()

                        if top_note == "ylang" and "ylang ylang" not in top_notes:
                                    top_note = "ylang ylang"
                        
                        top_note_kr = translator.translate(top_note, dest='ko').text

                        if top_note not in top_notes and top_note != "ylang":
                            top_notes.append(top_note)
                            sql = "INSERT INTO perfumescent (perfume_id, note_id, scent, scent_kr) VALUES (%s, %s, %s, %s)"
                            val = (j, 1, top_note, top_note_kr)
                            # print(val)
                            mycursor.execute(sql, val)
                    j += 1

            else:
                j += 1
            
            print('Top Notes:', top_notes)
            print('Middle Notes:', middle_notes)
            print('Base Notes:', base_notes, '\n')

            
    if brand_url is not None:
        perfume_urls = get_perfumeurl()
        if perfume_urls is not None:
            get_perfumeinfo(perfume_urls)


db_info.mydb.commit()