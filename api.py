from tinyrpc.dispatch import public
from call_logger import log_method_call
from selenium.webdriver.common.by import By


class Api(object):

    dispatcher = None
    browser = None

    def __init__(self, driver, dispatcher):
        self.browser = driver
        self.dispatcher = dispatcher
        self.component = pogoda(self.browser)
        self.dispatcher.register_instance(self.component, prefix='pogoda.')

    def __del__(self):
        self.browser.close()


class pogoda(object):

    def __init__(self, browser):
        self.browser = browser

    @log_method_call
    @public
    def dajdla(self, city):
        return self.get_from_accuwh(city)

    def get_from_accuwh(self, city):
        self.browser.get('https://www.accuweather.com/')
        try:
            self.browser.find_element(By.XPATH, "//*[contains(text(), 'Free with ads')]").click()
        except:
            pass

        self.browser.find_element_by_id('s').clear()
        self.browser.find_element_by_id('s').send_keys(city)
        self.browser.find_element_by_xpath('//button[@class="bt bt-go"]').click()

        try:
            self.browser.find_element_by_xpath("//div[@class='info']/h6/a").click()
        except:
            pass

        temp = self.browser.find_element_by_css_selector('span.large-temp').get_attribute("textContent").encode('ascii','ignore')
        cond = self.browser.find_element_by_css_selector('span.cond').text
        return temp + "*C; " + cond
