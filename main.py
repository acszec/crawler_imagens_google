import time
from selenium import webdriver
from scrapy import Selector
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import os
import progressbar

xpath_links_img = "//img[@class='n3VNCb']/@src"
xpath_thumbs = "//a[@class='wXeWr islib nfEiy mM5pbd']"

URL = "https://www.google.com/search?q=bitewing&tbm=isch&hl=en&hl=en&tbs=rimg%3ACaLAuIoxMlhQImADuZMFBjxWpzXfV52C3novyvlXA4jooohMLTci9lQPUCJR7LF6GcfFUR5GwjT60IjFDzMnAhlC2pcjnEH3YeOYwgi5BaZ87KPiGGymEqPfFXeoNUPewBw3rWlwp_1Oaq04qEgkDuZMFBjxWpxH6AX7HiPTDICoSCTXfV52C3novEWjUzYoyr_1lpKhIJyvlXA4jooogRTQMY5DyoEIIqEglMLTci9lQPUBH0dkwL3UPUsyoSCSJR7LF6GcfFEUEki2ZdkKWbKhIJUR5GwjT60IgRC71Crfg-fXAqEgnFDzMnAhlC2hE79WIqLAsSyCoSCZcjnEH3YeOYEcpzkfOub--zKhIJwgi5BaZ87KMRtopvEvtY-S4qEgniGGymEqPfFRFZv9aHGsfB3ioSCXeoNUPewBw3EaOO7Bgzlu6hKhIJrWlwp_1Oaq04R6EgzagfM3jJhesLrPRZxHu0&ved=0CBwQuIIBahcKEwiotNXI47HpAhUAAAAAHQAAAAAQCw&biw=2102&bih=947"
default_timeout = 1
max_images = 100
links_folder_name = 'links'


class Crawler(object):
    name = 'images'

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()

    def get(self, url):
        self.driver.get(url)

    def list_elements(self, xpath):
        return self.driver.find_elements_by_xpath(xpath_thumbs)

    def parse(self):
        list_thumbs = self.list_elements(xpath_thumbs)

        file_name = str(uuid.uuid1())
        os.makedirs(links_folder_name, exist_ok=True)
        file_path = os.path.join(links_folder_name, file_name)

        file = open(file_path, 'w')

        print(
            f"Initializing the scraping of {max_images} images and saving in file {file_path} \n")

        with progressbar.ProgressBar(max_value=max_images) as bar:
            for i, element_thumb in enumerate(list_thumbs):
                if i == max_images:
                    break

                try:
                    element_thumb.click()
                    time.sleep(default_timeout)
                    html = self.driver.page_source
                    src = get_link_img(html, xpath_links_img)

                    if src:
                        file.write(src)
                        file.write("\n")
                        bar.update(i)
                except:
                    pass

        file.close()
        self.close()

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
