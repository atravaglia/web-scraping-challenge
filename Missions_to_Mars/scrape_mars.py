# Dependencies
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Define database and collection
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
   
def scrape_info():
    browser = init_browser()
    # collection.drop()
    # listings = {}

# Nasa Mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    bs1 = bs(html,'html.parser')
    list_text = bs1.find("div",class_="list_text")
    title = list_text.find("div", class_="content_title").text
    para = bs1.find("div", class_="article_teaser_body").text

# JPL Mars Space Images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jhtml = browser.html
    jpl_soup = bs(jhtml,"html.parser")
    image_url = jpl_soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    base_link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    f_url = base_link+image_url
    featured_image_title = jpl_soup.find('h1', class_="media_feature_title").text.strip()
    
# Mars Facts
    web_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(web_url)
    mars_table_df = mars_table[0]
    mars_html = mars_table_df.to_html(header=False, index=False)

# Mars Hemispheres
    hemi_hurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_hurl)  
    hemi_html = browser.html 
    mh_soup = bs(hemi_html,"html.parser") 
    results = mh_soup.find_all(attrs = {"class" : "thumb"})
    hem_img_urls = []
    for result in results:
        image_url2 = result["src"]
        # image_url2 = image_url2.replace("/cache","")
        dictionary = {}
        # result_title = result.find('h3').text
        # end_link = result.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov"    
        # browser.visit(image_link)
        # html = browser.html
        # soup = bs(html, "html.parser")
        # downloads = soup.find("div", class_="downloads")
        # image_url = downloads.find("a")["href"]
        # print(result_title)
        # print(image_url)
        # dictionary['title']= result_title
        # dictionary['image_url']= image_url
        hem_img_urls.append( image_link+image_url2)



# Return results
    mars_data ={
		'title' : title,
		'para': para,
        'featured_url': f_url,
		'featured_image_title': featured_image_title,
		'mars_html': mars_html,
		'hem_imge_urls': hem_img_urls,
        'url': url,
        'jpl_url': jpl_url,
        'web_url': web_url,
        'hemi_hurl': hemi_hurl,
    }
    
    # Close the browser after scraping
    browser.quit()
   
    # Save into dictionary
    return mars_data

    
