import mysql.connector
import db_info

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import boto3
import re

mycursor = db_info.mydb.cursor()

dr = webdriver.Chrome()
dr.get('https://www.ottogi.co.kr/eng/product/product_list.asp#!')

def remove_html(sentence) :
	sentence = re.sub('(<([^>]+)>)', '', sentence)
	return sentence

def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="****",
            aws_secret_access_key="****",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3

# S3 버킷에 스크래핑 이미지 업로드
def upload_image_from_url(url, bucket_name, object_name):
    response = requests.get(url) # URL로부터 이미지 다운로드
    image_data = response.content    
    s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="****",
            aws_secret_access_key="****",
        )
    s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_name)

def clean_productname(product_name):
    product_name = product_name.replace(' ', '')
    return product_name

for p in range(1, 9):

    for t in range(1, 11):
        # 카테고리
        tag = dr.find_element(By.CSS_SELECTOR, '#all > div > ul > li:nth-child(' + str(t) + ') > div > div.card-content > p')
        category = tag.text
        print(category)

        if category!="Agriculture/Livestock/Fishery Products" and category!="Tea" and category!="Sauce/Vinegar/Ketchup/Mayo":
            # 제품 이름
            tag = dr.find_element(By.CSS_SELECTOR, '#all > div > ul > li:nth-child(' + str(t) + ') > div > div.card-content > span')
            product_name = tag.text
            print(product_name)

            # 제품 이미지
            tag = dr.find_element(By.CSS_SELECTOR, '#all > div > ul > li:nth-child(' + str(t) + ') > div > div.card-image > a > img')
            product_image = tag.get_attribute('src')
            print(product_image)

            # 제품 특징
            tag = dr.find_element(By.CSS_SELECTOR, '#all > div > ul > li:nth-child(' + str(t) + ') > div > div.card-reveal.center')
            product_info = tag.get_attribute('onclick')
            product_info_url = "https://www.ottogi.co.kr/eng/product/" + product_info[15:-1]
            html = requests.get(product_info_url).text
            soup = BeautifulSoup(html, "html5lib")
            
            product_feature = soup.select('#ottugiWrap > div.section > div > div.container.fix.recipe.mt50 > div.right > table > tbody > tr:nth-child(2) > td')
            product_feature = remove_html(str(product_feature))
            print(product_feature[1:-1])
            print("\n")

            sql = "INSERT INTO product (name_en, feature) VALUES (%s, %s)"
            val = (product_name, product_feature)
            mycursor.execute(sql, val)

            object_name = "product/" + clean_productname(product_name) + ".jpg"
            upload_image_from_url(product_image, "tpottogi", object_name)
        else:
            print("\n")
        
        element = dr.find_element(By.CSS_SELECTOR, '#all > ul > li:nth-child(' + str(p+1) + ') > a')
        element.click()

time.sleep(5)
dr.quit

db_info.mydb.commit()