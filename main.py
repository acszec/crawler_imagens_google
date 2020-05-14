import time
from selenium import webdriver
from scrapy import Selector

xpath_links_img = "//img[@class='n3VNCb']/@src"
xpath_thumbs = "//a[@class='wXeWr islib nfEiy mM5pbd']"

URL = "https://www.google.com/search?q=bitewing&tbm=isch&chips=q:bitewing,g_1:dental:W162ZKgq2os%3D&hl=en&ved=2ahUKEwiI9o2z47HpAhWzh54KHVsfA7oQ4lYoBHoECAEQHQ&biw=2102&bih=947#imgrc=fBdGhtajqipHGM"


class Crawler(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get(self, url):
        self.driver.get(url)

    def list_elements(self, xpath):
        return self.driver.find_elements_by_xpath(xpath_thumbs)

    def parse(self):
        list_thumbs = self.list_elements(xpath_thumbs)

        file = open('links.txt', 'w')

        for i, element_thumb in enumerate(list_thumbs):
            element_thumb.click()

            time.sleep(1)
            html = self.driver.page_source
            src = get_link_img(html, xpath_links_img)
            file.write(src)
            file.write("\n")
            print('image: {}'.format(i))

        file.close()

    def close(self):
        self.driver.quit()


def html_list(html, xpath):
    return Selector(text=html).xpath(xpath).extract()


def extract_content(html, xpath):
    value = Selector(text=html).xpath(xpath).extract()
    if value:
        return value[0]
    return value

def get_link_img(html, xpath):
    value = ""
    for src in html_list(html, xpath):
        if src.startswith("http://") or src.startswith("https://"):
            value = src
            break
    return value


crawler = Crawler()
crawler.get(URL)
crawler.parse()