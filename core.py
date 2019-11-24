import os

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from settings import (
    USE_TOR,
    TOR_EXE,
    TOR_PROFILE,
    PROXY_HOST,
    PROXY_PORT,
    FIREFOX_BINARY,
    USE_PROXY,
    HEADLESS,
)


class SeleniumDriver(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__driver = self.__create_driver()

    @property
    def driver(self):
        return self.__driver

    @staticmethod
    def __create_driver():
        binary = FirefoxBinary(FIREFOX_BINARY)

        options = Options()

        if HEADLESS:
            options.add_argument("--headless")

        if USE_TOR:
            os.popen(TOR_EXE)
            profile = FirefoxProfile(TOR_PROFILE)
        else:
            profile = FirefoxProfile()

        if USE_TOR or USE_PROXY:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.socks", PROXY_HOST)
            profile.set_preference("network.proxy.socks_port", PROXY_PORT)
            profile.set_preference("network.proxy.socks_remote_dns", False)

        profile.set_preference("dom.push.enabled", False)
        profile.update_preferences()

        return webdriver.Firefox(firefox_profile=profile,
                                 firefox_binary=binary,
                                 options=options)
