import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    title, body = mars_news(browser)
    
    data = {
        "news_title": title,
        "news_paragraph": body,
        "featured_image": mars_image(browser),
        "facts": mars_table(),
        "hemispheres": mars_hemispheres(browser),
    }
    browser.quit()
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.mars_db
    collection = db.mars 
    
    collection.insert_one(data)

def mars_table():

    #define url
    url = 'https://galaxyfacts-mars.com/'
    #returns table
    tables = pd.read_html(url)
    #create dataframe
    df = tables[0]

    new_header = df.iloc[0] 
    df = df[1:]
    df.columns = new_header

    return df.to_html(classes="table")


def mars_news(browser):
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


    url = 'https://redplanetscience.com/'
    browser.visit(url) 


    html = browser.html
    soup = bs(html, 'html.parser')

    title = soup.find(class_='content_title').text
    body = soup.find(class_='article_teaser_body').text


    return title, body


def mars_image(browser):

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)


    html = browser.html
    soup = bs(html, 'html.parser')



    image_href = soup.find("a", class_ = "showimg fancybox-thumbs")["href"]

    image_url = (f'https://spaceimages-mars.com/{image_href}')
    
    return image_url


def mars_hemispheres(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)



    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)

    hemisphere_images = []



    html = browser.html
    soup = bs(html, 'html.parser')

    image_links = soup.find_all("a", class_ = "itemLink product-item")

    for link in image_links:
        if link['href'] != '#':
            image_url = (f"https://marshemispheres.com/{link['href']}")
            image_title = link.text
            image_title = image_title.strip('\n')
            image_dict = {}
            image_dict = {'Url': image_url, 'Title': image_title}
            if image_dict['Title'] != '':
                hemisphere_images.append(image_dict)
    return hemisphere_images



if __name__ == "__main__":

    print(scrape_all())


