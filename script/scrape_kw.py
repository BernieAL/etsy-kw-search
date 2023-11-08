

from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

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



def write_to_csv(file_path,data):
    pass


def get_next_page(next_page_num):
    """
    Recieves next page num to visit, appends into url

    etsy has 21 page safety net - 
        if last page is 230, and you request pg 250, it will reroute to 230, 
        same if you req pg 251, 
        but if you try pg 252 you get "page not found".
        and so on for any pages after range of +21 from last page

    """
    try:
        prev_url =  driver.current_url
        driver.get(f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={next_page_num}&ref=pagination")
        curr_url = driver.current_url
        
        #LAST PAGE REDIRECT SAFETY NET
        # if we are at page n and try to go to page n+1, if we are brought back to page n again - we could be in the '+21 page safety net redirect'
            #try once more but with n+2 this time, if we are brought back to page n again, then we are in the safety net and page n is the LAST PAGE
        
        #if we tried to navigate to new url and its still the same as prev_url
        if prev_url == curr_url:
            #page n+2 check
            driver.get(f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={next_page_num+2}&ref=pagination")
            curr_url = driver.current_url
            #check again if new curr_url is still same as prev_url
            if prev_url == curr_url:
                return ("last page reached")
            
        #check page for notice saying "page not found" - this means there are no more pages for this search     
        pg_not_found = driver.find_element(By.XPATH,"//p[@contains='We couldn't find any results for pearl keychain']")
        
    except:
        pass

#TESTING
"""
assert function didnt throw any exceptions
assert url now has page num greater than prev url 
    Ex.
    compare:
        prev_url = (f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={2}&ref=pagination")
        curr_url = (f"https://www.etsy.com/search?q=pearl+keychain&explicit=1&order=price_desc&page={3}&ref=pagination")

"""
get_next_page()






def scrape_results_listings():
    """READ ME

        Runs on Etsy Search result listings page
        Called for each search results page visited
        Popultes child_listing_objects[] array
            each listing is encapsualted as an object and stored in the array for later use

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
    
    try:
        # search_bar = driver.find_element(By.ID,"global-enhancements-search-query")
        # search_bar.send_keys(term1 + Keys.RETURN)
        
        time.sleep(2)
        # result_container_div = driver.find_element(By.CLASS_NAME,"wt-bg-white wt-display-block wt-pb-xs-2 wt-mt-xs-0")
        
        
        # get parent list of all listings
        listing_parent_list = driver.find_element(By.XPATH,"//ol[contains(@class,'wt-grid')]")
        
        #from parent list, find all child elements 
        child_listings = listing_parent_list.find_elements(By.CLASS_NAME,"wt-list-unstyled")
        
        # FOR TESTING- shorten list for testing - REMOVE LATER
        child_listing_short = child_listings[:4]

        #dict to hold child objects with desired values
        child_listing_objects = []

        time.sleep(1)

        for child_el in child_listing_short:
            
            
            
            #GET STORE NAME, it doesnt work when combined as single statement
            # div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
            # print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)
            
            #free shipping indicator test - collect and mark if store offers free shipping
        
            child_obj = {
                'title':child_el.find_element(By.CLASS_NAME,"v2-listing-card__title").get_attribute('title'),
                'price':child_el.find_element(By.CLASS_NAME,"lc-price").text,
                'listing_link': child_el.find_element(By.CSS_SELECTOR,'a').get_attribute('href'),
                # 'store_name': div_containing_store_name = child_el.find_element(By.XPATH, "//div[contains(@class, 'wt-mb-xs-1')]")
                #             print(div_containing_store_name.find_element(By.XPATH,'//span[4]').text)
                # 'free_shipping': 
            }
            print(f"{child_obj} \n ----------  \n")
            child_listing_objects.append(child_obj)
            print(child_listing_objects)
    except NoSuchElementException as e:
        print(e)
#TESTING


def main_driver(term1='gold',term2='keychain',num_pages=2):
    
    term1 = 'busybabeshoppe'
    term2 = 'tote'

    

    # Ex. https://www.etsy.com/search?q=pearl%20keychain%20wristlet&ref=search_bar
    etsy_root_search_url = f'https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar'

    try:
        #navigate to root search URL
        driver.get(etsy_root_search_url)
        #root url counts as page 1
        curr_pg_num = 1

        #dict to hold child objects with scraped values
        child_listing_objects = []
        
        #curr pg = 1, we are on first page of search results
        while curr_pg_num < num_pages:
             
             #scrape data for each listing on current page
             scrape_results_listings(child_listing_objects)

             #navigate to next page, increment counter ahead of pg visit
             curr_pg_num+=1
             if(get_next_page(curr_pg_num))=='last page reached':
                 print("end of pages reached ahead of user request")
                 break;
             
        #write child_listing_obj to csv
        

    except:
        pass
    