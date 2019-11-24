from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core import SeleniumDriver
from scrapers import FBPostScraper
from settings import (
    FB_USERNAME,
    FB_PASSWORD,
    FB_MAINPAGE,
    POSTS_COUNT,
)


class FBCrawler(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__driver = SeleniumDriver().driver
        self.__driver.get(FB_MAINPAGE)
        self._auth()

    def _auth(self):
        assert "Facebook" in self.__driver.title
        try:
            elem = self.__driver.find_element_by_id("email")
            elem.send_keys(FB_USERNAME)
            elem = self.__driver.find_element_by_id("pass")
            elem.send_keys(FB_PASSWORD)
            elem.send_keys(Keys.RETURN)
        except NoSuchElementException:
            elem = self.__driver.find_element_by_name("email")
            elem.send_keys(FB_USERNAME)
            elem = self.__driver.find_element_by_name("pass")
            elem.send_keys(FB_PASSWORD)
            elem.send_keys(Keys.RETURN)

    def get_post_urls(self, find):
        self.__driver.get(FB_MAINPAGE)

        elem = self.__driver.find_element_by_name('q')
        elem.send_keys(find)
        elem.send_keys(Keys.RETURN)

        # Temp solution
        sleep(3)

        elem = self.__driver.find_element_by_tag_name(
            "li[data-edge='keywords_blended_posts']")
        elem.click()

        # Temp solution
        sleep(3)

        my_groups_button = self.__driver.find_elements_by_css_selector(
            "a[href*='/posts/']")[5]
        my_groups_button.click()

        # Temp solution
        sleep(3)

        last_height = self.__driver.execute_script(
            "return document.body.scrollHeight")
        post_urls = set()
        while len(post_urls) < POSTS_COUNT:
            posts = self.__driver.find_elements_by_css_selector(
                "a[href*='/posts/']")
            for post in posts:
                url = post.get_attribute('href')
                if url not in post_urls and url.split(
                        '/posts/')[-1].isnumeric():
                    post_urls.add(url)
            self.__driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            sleep(2)

            new_height = self.__driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return list(post_urls)[:POSTS_COUNT]

    def get_parsed_data(self, urls):
        parsed_posts = []
        for url in urls:
            self.__driver.get(url)
            html = self.__driver.page_source
            parsed_posts.append(FBPostScraper(html, url))
        return parsed_posts

    def close(self):
        self.__driver.quit()
