import mysql.connector
import requests
import boto3
import re

from bs4 import BeautifulSoup

# MySQL 서버와 연결
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="0128",
  database="scenchive"
)

# 쿼리 실행
mycursor = mydb.cursor()

mycursor.execute("SELECT brand_url FROM brand")
brand_url = mycursor.fetchall()
brand_url_list = [url[0] for url in brand_url]

mycursor.execute("SELECT brand_name FROM brand")
brand_name = mycursor.fetchall() # fetchall: 모든 검색 결과를 가져옴
brand_name_list = [list(brand_name[x]) for x in range(len(brand_name))] # tuple -> list


# HTML 내 브랜드 이미지 위치 추출
def get_brand_img_path(brand_url):
    url = "https://basenotes.com" + brand_url
    print(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    image_url_element = soup.select_one('#content > article > img')
    return image_url_element['src'] if image_url_element else None


# S3 버킷에 스크래핑 이미지 업로드
def upload_image_from_url(url, bucket_name, object_name):
    # 이미지 다운로드
    response = requests.get(url)
    image_data = response.content
    
    s3 = boto3.client('s3')
    s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_name)


# S3 버킷에 로컬 이미지 업로드
def upload_local_image_to_s3(local_image_path, bucket_name, object_name):
    s3 = boto3.client('s3')

    with open(local_image_path, 'rb') as image_file:
        s3.upload_fileobj(image_file, bucket_name, object_name)


# 파일명으로 사용 가능한 문자, 숫자만 남기고 나머지 문자 제거
def clean_filename(filename):
    cleaned_filename = re.sub(r'[^\w]', '', filename)
    return cleaned_filename


for brand_url in brand_url_list:
    image_url = get_brand_img_path(brand_url)

    if image_url is not None:
        bucket_name = "scenchive"
        brand_name = brand_name_list.pop(0)[0]
        object_name = "brand/" + clean_filename(brand_name) +  ".jpg" # S3에 저장될 파일명과 확장자

        if image_url == "https://basenotes.com/img/logo/":
            local_image_path = "D:\Project\Scenchive_SC\main\Scenchive\sample.png"
            print("url: " + local_image_path)
            print("bucket_name: " + bucket_name)
            print("object_name: " + object_name + "\n")
            upload_local_image_to_s3(local_image_path, bucket_name, object_name)
        else:
            url = image_url
            print("url: " + url)
            print("bucket_name: " + bucket_name)
            print("object_name: " + object_name + "\n")
            upload_image_from_url(url, bucket_name, object_name)

    else:
        brand_name_list.pop(0)[0]
        print("\n")
        
 