# Import Splinter and BeautifulSoup, and Pandas 
from splinter import Browser 
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set up Splinter // create instance of Splinter browser 
# **executable_path is unpacking dictionary we've stored path in
# headless =False means all browser's actions will be discplayed in 
# a Chrome window so we can see

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
slide_elem = news_soup.select_one("div.list_text")


# Begin scraping 
slide_elem.find("div", class_="content_title")

# Use the parent element (slide_elem) to find the first "a" tag and save it as "news_title" variable
news_title = slide_elem.find("div", class_="content_title").get_text()
news_title


# Now pull summary 
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images 

# Visit URL 
url = "https://spaceimages-mars.com"
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ## Mars Facts

# Scrape table using pandas .read_html() function

df = pd.read_html("https://galaxyfacts-mars.com/")[0]
df.columns=["description", "Mars", "Earth"]
df.set_index("description", inplace=True)
df


# Convert back to html 
df.to_html()


browser.quit()





