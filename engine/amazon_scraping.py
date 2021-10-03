from math import asin
from bs4 import BeautifulSoup as bs
import re

from selenium.webdriver import Chrome
from common.driver import set_driver

AMAZON_DOMAIN = "https://www.amazon.co.jp/"

class AmazonItem():

    def __init__(self, name:str=None, description:str=None, price:int=None, 
                 asin:str=None, star:float=None):
        self.name = name
        self.description = description
        self.price = price
        self.asin = asin
        self.star = star

class AmazonScraping():

    def __init__(self):
        self.driver = set_driver()


    def fetch_item(self, url: str):
        self.driver.get(url)

        name = self.driver.find_element_by_css_selector('#productTitle').text
        description = self.driver.find_element_by_css_selector('#productDescription_feature_div').text
        price = self.driver.find_element_by_css_selector('#priceblock_ourprice').text.replace('￥', '').replace(',', '')
        star = self.driver.find_element_by_css_selector('.a-icon-alt').text.replace('5つ星のうち', '')

        m = re.search(r'/dp/(\w{10})', url)
        if m:
            asin = m.group(1)
        else:
            asin = None

        item = AmazonItem(
            name=name,
            description=description,
            price=price,
            star=star,
            asin = asin
        )

        return item

    
    def fetch_ranking_items(self, url: str, limit:int=50):
        self.driver.get(url)

        # スペースを開けると配下という意味になる
        # 直下は>
        item_elms = self.driver.find_elements_by_css_selector('.aok-inline-block.zg-item > a')

        item_links = []
        for item_elm in item_elms[:limit]:
            item_link = item_elm.get_attribute('href')
            item_links.append(item_link)

        items = []
        for item_link in item_links:
            try:
                item = self.fetch_item(item_link)
                items.append(item)
                print(item.name)
            except Exception as e:
                print(e)
        
        return items