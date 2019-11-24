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
        """ Паттерн Singleton для использования одного паука """

        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__driver = SeleniumDriver().driver
        self.__driver.get(FB_MAINPAGE)
        self._auth()

    def _auth(self):
        """ Метод для авторизации на Facebook """

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
        """ Метод для получения ссылок на публикации по строке поиска """

        find = find.replace(' ', '%20')
        self.__driver.get(f'{FB_MAINPAGE}search/posts/?q={find}')

        my_groups_button = self.__driver.find_elements_by_css_selector(
            "a[href*='/posts/']")[5]
        my_groups_button.click()

        # Temp solution
        sleep(5)

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
        """ Метод получения обработанных постов по списку ссылок """

        parsed_posts = []
        for url in urls:
            self.__driver.get(url)
            elem = self.__driver.find_element_by_class_name(
                'userContentWrapper')
            html = elem.get_attribute("outerHTML")
            parsed_posts.append(FBPostScraper(html, url))
        return parsed_posts

    def close(self):
        """ Метод закрытия браузера """

        self.__driver.quit()
