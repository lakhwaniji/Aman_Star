import requests
from bs4 import BeautifulSoup
import csv


def create_product_url(name):
    link=None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    search_query = name.replace(' ', '+')
    base_url = f'''https://www.amazon.com/s?k={search_query}'''
    response = requests.get(base_url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    for result in results[0:10]:
        data=result.find('span',{'class':'puis-label-popover-default'})
        if data is None:
            link = result.find(('a'), {'class': 'a-link-normal'}).get("href")
            link = "https://www.amazon.com" + link
            break
    return link


def get_data(product_link):
    product_data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    response = requests.get(product_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = soup.find('tr', {'class': 'po-brand'})
    if(result is not None):
        raw_data = result.text
        raw_data = raw_data.strip(" ")
        raw_data = raw_data.split(" ")
        product_data["Brand"] = raw_data[-1]
    else:
        product_data["Brand"]="No value found"

    result = soup.find('span', {'class': 'a-size-large product-title-word-break'})

    if (result is not None):
        raw_data = result.text
        raw_data = raw_data.strip(" ")
        product_data["Model_Info"] = raw_data
    else:
        product_data["Model_Info"]="No value found"

    result = soup.find('div', {'class': 'a-section a-spacing-medium a-spacing-top-small'})
    if result is not None:
        raw_data = result.text
        raw_data = raw_data.strip(" ")
        product_data["Model_Details"] = raw_data
    else:
        product_data["Model_Details"]="No value found"
    result=soup.find('img',{'class':'a-dynamic-image'}).get("src")
    if result is not None:
        product_data['Image_Link'] = result
    else:
        product_data["Image_Link"] = "No value found"
    return (product_data)


def add_data(product_info,file):
    # Open the CSV file in "append" mode
    file="Data/"+file
    with open(file, 'a', newline='') as f:
        # Create a dictionary writer with the dict keys as column fieldnames
        writer = csv.DictWriter(f, fieldnames=product_info.keys())
        writer.writerow(product_info)
    return "Success"
