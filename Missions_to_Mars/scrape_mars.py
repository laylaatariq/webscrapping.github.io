#Libraries
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#Dictionary to store the scrapped data
scrapped_data = {}

#Scrapping function
def scrape():
    #Url to scrape
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    #Asking chromedriver to control the website
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Getting the title of the latest news on the page
    search = soup.body.find('div', class_='content_title')

    for x in search.find_all('a'):
        news_title = x.get_text()
    
    #Adding the data into the dictionary
    scrapped_data['news_title'] = news_title

    #Getting the body of the news article
    news_b = soup.body.find('div', class_='article_teaser_body')
    news_p = news_b.get_text()

    #Adding the body of the article into the dictionary
    scrapped_data['news_body'] = news_p

    #Adding the new image url to scrape the link for the img
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    image_html = browser.html
    image = BeautifulSoup(image_html, 'html.parser')

    img_url = image.body.find('div', class_='carousel_container')

    for x in img_url.find_all('a'):
        img= x.get('data-fancybox-href')
    
    head_url = "https://www.jpl.nasa.gov"
    featured_image_url = head_url + img

    #Adding the image url into the dictionary
    scrapped_data['featured_img_url'] = featured_image_url

    #Getting the weather data
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    weather_html = browser.html
    weather = BeautifulSoup(weather_html, 'html.parser')

    weather_soup = weather.body.find('div', class_= 'js-tweet-text-container')

    for x in weather_soup.find_all('p'):
        mars_weather = x.get_text()
    
    mars_weather = mars_weather[:165]

    #Adding weather information in the dictionary
    scrapped_data['mars_weather'] = mars_weather

    #Getting the mars facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    facts_html = browser.html
    facts = BeautifulSoup(facts_html, 'html.parser')

    facts_soup = facts.body.find('div', class_='site-content')

    facts_list = []
    for x in facts_soup.ul.find_all('strong'):
        fact = x.get_text()
        facts_list.append(fact)

    #Adding the list into the dictionary
    scrapped_data['facts'] = facts_list

    #Getting Mars Description
    fact_table = facts.body.find('table', class_='tablepress')

    l = []
    for x in fact_table.find_all('tr'):
        td = x.find_all('td')
        row = [x.text for x in td]
        l.append(row)

    #Storing the table into a dataframe
    facts_df = pd.DataFrame(l, columns=['Fact', 'Measurement'])

    #Converting the dataframe to a html table
    facts_table = facts_df.to_html(header=False, index=False)

    #Adding the Mars description table to the dict
    scrapped_data['mars_table'] = facts_table

    #Getting the Hemisphere Names and Images
    hemisphere_image_urls = []
    url_front = "https://astropedia.astrogeology.usgs.gov/download/"
    url_end = ".tif/full.jpg"

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    hemi_html = browser.html
    hemi = BeautifulSoup(hemi_html, 'html.parser')

    hemi_soup = hemi.body.find('div', class_='results')


    for j in hemi_soup.find_all('div', class_='description'):
        urls = j.find_all('a')
        title = [t.text for t in urls]
        title = ''.join(title)
        link = [u.get('href') for u in urls]
        link_new = ''.join(link)
        link_new = link_new[12:]
        full_url = url_front + link_new + url_end
        hemi_dict = {'title' : title, 'img_url': full_url}
        hemisphere_image_urls.append(hemi_dict)
    
    #Adding the list of dictionary to the dict
    scrapped_data['hemisphere'] = hemisphere_image_urls

    #Quitting the browser after all the scrapping has been done
    browser.quit()

    #Returning the data
    return scrapped_data