'''
Given a feild and location return
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from linked_in_profile import LinkedInProfile

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)


def get_driver(url):
    prof = webdriver.FirefoxProfile()
    prof.set_preference("general.useragent.override",
                        "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
    browser = webdriver.Firefox(prof)
    set_viewport_size(browser, 800, 600)
    browser.implicitly_wait(15)
    browser.get(url)
    return browser

def get_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

class Scrapey():
    def __init__(self, username, password, feild, location):
        self.username = username
        self.password = password
        self.feild = feild
        self.location = location

    def login(self, browser):
        username = browser.find_element_by_id("username")
        username.clear()
        username.send_keys(self.username)
        browser.implicitly_wait(15)
        password = browser.find_element_by_id('password')
        password.clear()
        password.send_keys(self.password)
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

    def get_profile_links(self, browser):
        search = browser.find_element_by_id('search-input')
        search.clear()
        search.send_keys(self.feild + " AND " + self.location)
        search.submit()
        time.sleep(5)
        browser.refresh()
        soup = get_html(browser.page_source)
        items= soup.find_all(attrs={"data-result-component-type" : "PRIMARY"})
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

if __name__ == "__main__":
    scrapey = Scrapey('jack.betcher@gmail.com', 'Crazyarm1a', 'software engineer', 'Boston')

    '''Single instance of driver used to login and get list of profiles'''
    browser = get_driver("https://www.linkedin.com/login")
    login_cookies = scrapey.login(browser)
    profile_links = scrapey.get_profile_links(browser)
    browser.close()

    linked_in_profiles = []

    for link in profile_links:
        profile = LinkedInProfile(link, login_cookies)
        '''This is where multi threading can provide speed up'''
        profile.get_profile_info()
        linked_in_profiles.append(profile)
    for prof in linked_in_profiles:
        if prof.name and prof.location and prof.title:
            print(prof.name + " " + " " + prof.title)
        else:
            print(prof.name)
            print(prof.link)
            print('++++++++++++++++++++++')


