from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import random
import time

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def get_driver(url, cookies):
    prof = webdriver.FirefoxProfile()
    prof.set_preference("general.useragent.override",
                        "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
    browser = webdriver.Firefox(prof)

    set_viewport_size(browser, random.randint(600,800), random.randint(600,800))


    browser.implicitly_wait(5)
    browser.get('https://www.linkedin.com')
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.implicitly_wait(2)
    browser.get(url)
    browser.implicitly_wait(3)
    return browser


def get_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


class LinkedInProfile():
    def __init__(self, url, cookies):
        self.link = url
        #pass these so we stay logged in
        self.driver_cookies = cookies
        self.name = None
        self.education = None
        self.username = None
        self.title = None
        self.current_role = None
        self.location = None


    def get_profile_info(self):
        #Scrape profile to get information
        browser = get_driver(self.link, self.driver_cookies)
        soup = get_html(browser.page_source)

        try:
            items = soup.find_all('span', {'dir': 'ltr'})
            self.name = items[0].get_text()
            self.education = items[1].get_text()
            self.current_role = items[2].get_text()
            self.title = items[3].get_text()
        except Exception as e:
            print(e)
            print("Unable to extract profile information for " + self.link)
            return False
        browser.close()
        return True



