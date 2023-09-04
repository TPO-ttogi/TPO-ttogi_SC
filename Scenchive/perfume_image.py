import db_info
import requests
import boto3
import re
import unicodedata

from bs4 import BeautifulSoup


# 쿼리 실행
mycursor = db_info.mydb.cursor()
mycursor.execute("SELECT brand_url FROM brand WHERE id>=601 and id<=682")
result = mycursor.fetchall() # fetchall: 모든 brand_url 검색 결과를 가져옴
result = [list(result[x]) for x in range(len(result))] # tuple -> list


# HTML 내 향수 이미지 URL 추출
def get_perfume_img_path(perfume_url):
    url = perfume_url
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    image_url_element = soup.select_one('#content > article > div.product_image > img')
    return image_url_element['src'] if image_url_element else None

def get_perfume_name(perfume_url):
    url = perfume_url
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    perfume_name_element = soup.select_one('#fraghead > div > div > div > div > h1 > span:nth-child(1)')
    return perfume_name_element.get_text() if perfume_name_element else None

# S3 버킷에 스크래핑 이미지 업로드
def upload_image_from_url(url, bucket_name, object_name):
    response = requests.get(url)
    image_data = response.content 
    s3 = boto3.client('s3')
    s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_name)

# S3 버킷에 로컬 이미지 업로드
def upload_local_image_to_s3(local_image_path, bucket_name, object_name):
    s3 = boto3.client('s3')
    with open(local_image_path, 'rb') as image_file:
        s3.upload_fileobj(image_file, bucket_name, object_name)

# 파일명 형식 수정
def clean_filename(filename):
    cleaned_filename = re.sub(r'[^\w]', '', filename) # 파일명으로 사용 가능한 문자, 숫자만 남기고 나머지 문자 제거
    cleaned_filename = unicodedata.normalize('NFKD', cleaned_filename).encode('ASCII', 'ignore').decode('utf-8') # è, é, ê, ë를 모두 'e'로 변환
    return cleaned_filename


for i in result:
    brand_url = i[0]
    # print(brand_url)
    
    # perfume 상세 페이지 URL 스크래핑
    def get_perfumeurl():

        #1) 브랜드 상세 페이지 접근
        brandpage_url = "https://basenotes.com" + brand_url
        # print(brandpage_url)
        html = requests.get(brandpage_url).text
        soup = BeautifulSoup(html, "html5lib")
        
        #2) yearheading 클래스 태그 찾기
        yearheading_elements = soup.find_all(class_='yearheading')

        #3) yearheading 클래스 내부의 a 태그 찾기
        for yearheading_element in yearheading_elements:
            a_tags = yearheading_element.find_all('a')
            for a_tag in a_tags:
                perfume_url = a_tag['href']
                image_url = get_perfume_img_path(perfume_url)
                
                if image_url is not None:
                    bucket_name = "scenchive"
                    perfume_name = get_perfume_name(perfume_url)
                    object_name = "perfume/" + clean_filename(perfume_name.rstrip()) +  ".jpg" # S3에 저장될 파일명과 확장자
                    
                    if image_url == "https://basenotes.com/img/product/" or image_url == "https://basenotes.com/img/product/26122876-4267-j":
                        local_image_path = "D:\Project\Scenchive_SC\main\Scenchive\sample.png"
                        print("brand: " + brand_url)
                        print("url: " + local_image_path)
                        print("object_name: " + object_name + "\n")
                        upload_local_image_to_s3(local_image_path, bucket_name, object_name)
                    else:
                        url = image_url
                        print("brand: " + brand_url)
                        print("url: " + url)
                        print("object_name: " + object_name + "\n")
                        upload_image_from_url(url, bucket_name, object_name)

        print('\n')

            
    if brand_url is not None:
        perfume_urls = get_perfumeurl()
        
 