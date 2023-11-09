# etsy-kw-search

###
This tool is for performing an etsy search and scraping the details off of the resulting listings

## Purpose:
User can collect and analyze results for possible keywords they are considering for their listing
#Ex. 
  * User wants to sell Pearl keychain
  * User wants to know details about listings that result from searching "Pearl keychain"
  * Details such as:
    keywords in title used by competitors (most common, outliers etc)
    stores that have the most listings appearing under given search term
    Avg,Hi,Low, listing prices for similar items
    If Freeshipping is offered

  * With these details, the user can determine if their original search term is worth including in
  their listing titles - allowing them to save time and avoid saturated or dead-end search terms
  ---------------
  term_1 = "Pearl" <br>
  term_2 = "keychain" <br>
  pages_to_visit = 4 <br>
  etsy_root_search_url = f'https://www.etsy.com/search?q={term1}%20{term2}&ref=search_bar' <br>
  main_driver(term_1,term_2,pages_to_visit)
  
  

## How It Works
1. Script accepts user search terms and desired number of pages to visit
2. Embed the search terms into the etsy target url as a template string
3. Using chromedriver, it executes navigation for this search result
4. For each page visited, Scrapes details from resulting listings and appends to array 
5. Array is then written to file for analysis


