'''
Given a feild and location return
'''
import re
import request_headers
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from linked_in_profile import LinkedInProfile

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

#
# def get_driver(url):
#     prof = webdriver.FirefoxProfile()
#     prof.set_preference("general.useragent.override", "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
#     browser = webdriver.Firefox(prof)
#     set_viewport_size(browser, 800, 600)
#     browser.implicitly_wait(15)
#     browser.get(url)
#     return browser

def get_driver(url, cookies=[]):
    prof = webdriver.FirefoxProfile()
    headers = request_headers.get_headers()
    user_agent = request_headers.get_random_user_agent()
    prof.set_preference("general.useragent.override", user_agent)
    browser = webdriver.Firefox(prof)

    set_viewport_size(browser, random.randint(1000,1200), random.randint(500,600))


    browser.implicitly_wait(5)
    browser.get('https://www.linkedin.com')
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.implicitly_wait(2)
    browser.get(url)
    browser.implicitly_wait(3)
    return browser

def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def get_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def random_sleep():
    time.sleep(random.randint(1,5))

class Scrapey():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, browser):
        username = browser.find_element_by_id("username")
        username.clear()
        username.send_keys(self.username)
        random_sleep()
        password = browser.find_element_by_id('password')
        password.clear()
        password.send_keys(self.password)
        random_sleep()
        browser.find_element_by_class_name("login__form_action_container").click()
        cookies = browser.get_cookies()
        return cookies

    def get_search_results(self, search_url):
        soup = get_html(search_url)
        for line in soup:
            print(line)
        people = soup.findAll('span', {'class': 'name actor-name'})
        print(people)
        return people

    def get_profile_links(self, login_cookies, field, location):
        browser = get_driver("https://www.linkedin.com/", login_cookies)

        search = browser.find_element_by_xpath('//input[@placeholder="Search"]')
        #search = browser.find_element_by_id('search-input')
        search.clear()
        search.send_keys(field + " AND " + location)
        random_sleep()
        search.send_keys(Keys.ENTER)
        random_sleep()
        soup = get_html(browser.page_source)
        #Social Impact Maarketing Associate II at Vettery
        items= soup.find_all(attrs={"data-test-search-result" : "PROFILE"})

        profiles = []
        for item in items:
            try:
                profiles.append('http://linkedin.com/' + item.find("a", {"href" : True}).get("href") + '?trk=people-guest_people_search-card')
            except Exception:
                print("Unable to extract link for profile")
                continue
            '''Leave the parsing of the information for the threads'''
            #spans = item.find_all("span", {"dir": "ltr"})
            #info = [span.get_text() for span in spans]
            #profiles[info[0]] = {"title" : info[1], "profile": profile}
        return profiles

    def send_message(self, recipient, message, cookies):
        #Need to navigate to messages where browser is on messaging paige
        browser = get_driver('https://www.linkedin.com/messaging/compose/', cookies)
        #web_element = browser.find_element_by_tag_name("body")
        try:
            browser.implicitly_wait(3)
            web_element = browser.find_element_by_xpath('//input[@placeholder="Type a name or multiple names…"]')
            web_element.click()
            web_element.clear()
            web_element.send_keys(recipient)

            random_sleep()

            web_element.send_keys(Keys.ENTER)

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            random_sleep()

            web_element2 = browser.find_element_by_xpath('//div[@aria-label="Write a message…"]')

            random_sleep()

            web_element2.click()

            web_element2.send_keys(message)

            web_element3 = browser.find_element_by_xpath('//button[@type="submit"]')
            random_sleep()
            web_element3.click()
        except Exception as e:
            print(e)
        return True

    def add_user(self, login_cookies, profile_link):
        browser = get_driver(profile_link, login_cookies)
        random_sleep()
        try:
            connect = browser.find_element_by_xpath('//button[contains(@aria-label,"Connect with")]')
            random_sleep()
            connect.click()
        except Exception as e:
            print(e)






