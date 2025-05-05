from selenium import webdriver
from selenium import By
from selenium import Keys
from selenium import WebDriverWait
from selenium import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, driver_path, browser="chrome"):
        if browser.lower() == "chrome":
            self.driver = webdriver.Chrome(executable_path=driver_path)
        elif browser.lower() == "firefox":
            self.driver = webdriver.Firefox(executable_path=driver_path)
        else:
            raise ValueError("Unsupported browser. Use 'chrome' or 'firefox'.")

    def open_url(self, url):
        self.driver.get(url)

    def findByCSS(self, css_selector):
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)
    
    def findByXPath(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)
    
    def findByTagName(self, tag_name):
        return self.driver.find_element(By.TAG_NAME, tag_name)
    
    def click_element(self, element):
        self.execute_script("arguments[0].click();", element)


    def send_keys(self, by, value, keys):
        element = self.find_element(by, value)
        element.send_keys(keys)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def close_browser(self):
        self.driver.quit()

