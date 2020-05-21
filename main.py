import time
from selenium import webdriver
from scrapy import Selector
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import os
import progressbar
import sys

xpath_links_img = "//a[@role='link']/img[@class='n3VNCb']/@src"
xpath_thumbs = "//a[@class='wXeWr islib nfEiy mM5pbd']"
xpath_input_more_results = "//input[@class='mye4qd'][contains(@value, 'more results')]"
src_default_google = ['//encrypted', 'jpeg;base64']

default_timeout = 1
links_folder_name = 'links'


class Crawler(object):
    name = 'images'

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get(self, url):
        self.driver.get(url)

    def list_elements(self, xpath):
        for i in range(1,11):
            time.sleep(2)
            self.driver.execute_script(
                """
                content = document.getElementById('islmp');
                content.scrollIntoView(false);
                """)

            print(f"->Scrolling to bottom {i}\n")
            try:
                time.sleep(2)
                more_results = self.driver.find_element_by_xpath(xpath_input_more_results)
                more_results.click()
                print(f"->Clicking load more results\n")
            except:
                pass

        print(f"[ Scrolling finished ]\n")
        return self.driver.find_elements_by_xpath(xpath_thumbs)

    def parse(self):
        list_thumbs = self.list_elements(xpath_thumbs)
        total_images = len(list(enumerate(list_thumbs)))

        file_name = str(uuid.uuid1())
        os.makedirs(links_folder_name, exist_ok=True)
        file_path = os.path.join(links_folder_name, file_name)

        file = open(file_path, 'w')

        print(
            f"Initializing the scraping of {total_images} images and saving in file {file_path} \n")

        with progressbar.ProgressBar(max_value=total_images) as bar:
            for i, element_thumb in enumerate(list_thumbs):
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
    for i, src in enumerate(html_list(html, xpath)):
        # if '.jpg' in src.lower() or '.png' in src.lower() or '.jpeg' in src.lower():
        if src_default_google[0] not in src.lower() and src_default_google[1] not in src.lower():
            value = src
            break
    return value


if __name__ == "__main__":
    file_path = sys.argv[1]
    print(f"Starting the crawler of all the links of file {file_path}")

    if not os.path.isfile(file_path):
        print("File path {} does not exist. Exiting...".format(file_path))
        sys.exit()

    with open(file_path) as fp:
        urls = [url for url in enumerate(fp)]

    for i, url in urls:
        crawler = Crawler()
        crawler.get(url)
        crawler.parse()