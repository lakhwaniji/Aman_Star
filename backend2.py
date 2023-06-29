from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv

def create_product_url(name):
    if name =="":
        return None
    base_url = f'https://gear-up.me/#/dfclassic/query={name}&query_name=match_and'
    driver = webdriver.Chrome()
    driver.get(base_url)
    time.sleep(3)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    result=soup.find("a",{"class":"df-card__main"}).get("href")
    driver.quit()
    return result
def get_data(product_link):
    if product_link == "":
        return None
    driver = webdriver.Chrome()
    base_url = product_link
    driver.get(base_url)
    time.sleep(3)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    product_data= {}

    result=soup.find("h1",{'class':'product-name'}).text
    product_data["Brand"]=""
    product_data["Model_Info"]=result

    result=soup.find("div",{"class":"std"})
    product_data["Model_Details"]=result.text

    result=soup.find("img",{"id":"ori_image"})
    product_data["Image_Link"]=(result.get("src"))
    driver.quit()

    return product_data

def add_data(product_info,file):
    # Open the CSV file in "append" mode
    file="Data/"+file
    with open(file, 'a', newline='') as f:
        # Create a dictionary writer with the dict keys as column fieldnames
        writer = csv.DictWriter(f, fieldnames=product_info.keys())
        writer.writerow(product_info)
    return "Success"



