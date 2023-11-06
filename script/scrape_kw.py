

from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(executable_path=r'C:\browserdrivers\chromedriver\chromedriver.exe')
driver = webdriver.Chrome()

    


term1 = 'pearl'
term2 = 'keychain'

# Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
etsy_root_search_url = f'https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar'


driver.get(etsy_root_search_url)


try:
    # search_bar = driver.find_element(By.ID,"global-enhancements-search-query")
    # search_bar.send_keys(term1 + Keys.RETURN)
    
    time.sleep(2)
    # result_container_div = driver.find_element(By.CLASS_NAME,"wt-bg-white wt-display-block wt-pb-xs-2 wt-mt-xs-0")
    
    
    # get parent list of all listings
    listing_parent_list = driver.find_element(By.XPATH,"//ol[contains(@class,'wt-grid')]")
    
    #from parent list, find all child elements 
    child_listings = listing_parent_list.find_elements(By.CLASS_NAME,"wt-list-unstyled")
    
    # shorten list for testing - RMEOVE LATER
    child_listing_short = child_listings[:6]

    #dict to hold child objects with desired values
    child_listing_objects = {}

    """
    child_el is list element nested in parent OL
    title,price,listing_link are all extracted and put into a child_obj, which is put into a dict of child_objects
    """
    for child_el in child_listing_short:
        child_obj = {
            'title':child_el.find_element(By.CLASS_NAME,"v2-listing-card__title").get_attribute('title'),
            'price':child_el.find_element(By.CLASS_NAME,"lc-price").text,
            'listing_link': child_el.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
        }
        





except NoSuchElementException as e:
    print(e)

