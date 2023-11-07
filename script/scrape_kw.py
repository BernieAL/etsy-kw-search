

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


#UTIL AND NAV FUNCTIONS
"""
navigate to next page - can be done using url or clicking page buttons
url for pagination: 
    https://www.etsy.com/search?q=pearl+keychain&ref=pagination&page=2

QUESTIONS:
    what if there isnt page number n? how to handle that - like if theres only 3 pages and we try to request 4? 
    if this happens:
        etsy returns a page that says "we couldnt find any resutls for pearl keychain"
    we would write conditonal logic to check for:
        -"we couldnt find any resutls for pearl keychain"
    at which point we know the page doesnt exist if we get this message
"""

pages_to_visit = 3

# def main_driver(pages_to_visit):
        
#         curr_pg_num = 1
#         while curr_pg_num < pages_to_visit:
#              get_next_page(curr_pg_num+1)

#             #call to scraping logic on new page


# def get_next_page(pages_to_visit):
#     driver.get('https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page=120&ref=pagination')


term1 = 'busybabeshoppe'
term2 = 'tote'

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
    child_listing_objects = []

    """
    child_el is list element nested in parent OL
    title,price,listing_link are all extracted and put into a child_obj, which is put into a dict of child_objects

        Ex.
        child_listing_objects = [
            {
                'title':'Pearl keychain', 
                'price':'4.99',
                'link':<link>},
            }
        ]

    """
    time.sleep(2)
    for child_el in child_listing_short:
        
        # child_el.find_element(By.XPATH,"//p>span[contains(text(), 'From shop')]").text) #DOESNT WORK YET

        div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
        spans = div_containing_store_name.find_elements(By.TAG_NAME,'span')
        for span in spans:
            print(span.text)

        # child_obj = {
        #     'title':child_el.find_element(By.CLASS_NAME,"v2-listing-card__title").get_attribute('title'),
        #     'price':child_el.find_element(By.CLASS_NAME,"lc-price").text,
        #     'listing_link': child_el.find_element(By.CSS_SELECTOR,'a').get_attribute('href'),
        #     'store_name': child_el.find_element(By.XPATH,"//span[contains(text(), 'From shop')]").text) #DOESNT WORK YET
        # }
        # # print(child_obj)
        # print('------------')
        # child_listing_objects.append(child_obj)
        # print(child_listing_objects)
except NoSuchElementException as e:
    print(e)




