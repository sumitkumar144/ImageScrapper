import os
import time
import requests
from selenium import webdriver

class ImageScrapperService:
    def fetch_image_urls(self,query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

            # build the google query

        self.search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        wd.get(self.search_url.format(q=query))

        self.image_urls = set()
        self.image_count = 0
        self.results_start = 0
        while self.image_count < int(max_links_to_fetch):
            scroll_to_end(wd)

            # get all image thumbnail results
            self.thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            self.number_results = len(self.thumbnail_results)

            print(f"Found: {self.number_results} search results. Extracting links from {self.results_start}:{self.number_results}")

            for self.img in self.thumbnail_results[self.results_start:self.number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    self.img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                self.actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for self.actual_image in self.actual_images:
                    if self.actual_image.get_attribute('src') and 'http' in self.actual_image.get_attribute('src'):
                        self.image_urls.add(self.actual_image.get_attribute('src'))

                self.image_count = len(self.image_urls)

                if len(self.image_urls) >= int(max_links_to_fetch):
                    print(f"Found: {len(self.image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(self.image_urls), "image links, looking for more ...")
                time.sleep(30)
                return
                self.load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if self.load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            self.results_start = len(self.thumbnail_results)

        return self.image_urls

    def persist_image(self,folder_path: str, url: str, counter):
        try:
            self.image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
            f.write(self.image_content)
            f.close()
            print(f"SUCCESS - saved {url} - as {folder_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

    def list_only_jpg_files(self, folder_name):
        self.list_of_jpg_files = []
        self.list_of_files = os.listdir(folder_name)
        print('list of files==',self.list_of_files)
        #print(self.list_of_files)
        for self.file in self.list_of_files:
            self.name_array = self.file.split('.')
            print("Name Arraye",self.name_array)
            if (self.name_array[1] == 'jpg'):
                self.list_of_jpg_files.append(self.file)
            else:
                print('filename does not end with jpg')
        return self.list_of_jpg_files

