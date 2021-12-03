# Import Splinter and BeautifulSoup, and Pandas 
from splinter import Browser 
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Create function to initialize browser, create data dictionary, 
# and end the WebDriver, return scraped data 
def scrape_all():
    # Initiate headless driver for deployment -- scraping behind the scenes
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Assign variables using mars_news function
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":hemisphere_images(browser)
    }

    # Stop webdriver and return data 
    browser.quit()
    return data 




# Set up Splinter // create instance of Splinter browser 
# **executable_path is unpacking dictionary we've stored path in
# headless =False means all browser's actions will be discplayed in 
# a Chrome window so we can see

# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the Mars NASA site 
    url ='https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading page 
    # 1) Sets <ul class="item_list"> as ul.item_list format
    # 2) Delay helps as dynamic pages with images can take a bit to load
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up HTML parser 
    html = browser.html 
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Begin scraping 
        slide_elem = news_soup.select_one("div.list_text")

        # Use the parent element (slide_elem) to find the first "a" tag and save it as "news_title" variable
        news_title = slide_elem.find("div", class_="content_title").get_text()

        # Now pull summary 
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
        
    return news_title, news_p


# ### Featured Images 

def featured_image(browser):
    # Visit URL 
    url = "https://spaceimages-mars.com"
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts

def mars_facts():
    # Scrape table using pandas .read_html() function
    try:
        df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None 

    df.columns=["description", "Mars", "Earth"]
    df.set_index("description", inplace=True)
    
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If  running as script, print scraped data
    print(scrape_all())


# ## HEMISPHERE IMAGES 

def hemisphere_images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the resulting html with soup
    html = browser.html
    mars_soup = soup(html, 'html.parser')
    # mars_soup


    pics = mars_soup.find_all('img', class_='thumb')

    for pic in pics:
        mars_url_rel = pic.get('src')
        mars_url = f'https://marshemispheres.com/{mars_url_rel}'
        mars_title =pic.get('alt')

        dict = {'img_url':mars_url, 'title':mars_title}
        dict_copy = dict.copy()

        hemisphere_image_urls.append(dict_copy)


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls




