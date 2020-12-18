#!/usr/bin/env python
# coding: utf-8

# # Project Amazon Price Tracker
# # Akbar Azad

# In[24]:


from requests_html import HTMLSession
import csv
import datetime as datetime
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd


# In[25]:


#s = HTMLSession()
#r = s.get('https://www.amazon.com/dp/1118345606')
#price = r.html.find('#buyNewSection > div > div > span > span')[0].text
#price.replace('S$', '').replace(',', '').strip()
#title = r.html.find('#productTitle')[0].text.strip()


# In[26]:


def amazon_price_tracker(_asin_isbn):
    _asin_isbn = str(_asin_isbn)
    url = f'https://www.amazon.sg/dp/{_asin_isbn}'
    #session = HTMLSession()
    #request = session.get(url)
    driver = webdriver.Chrome(executable_path = r'C:\Users\65961\Desktop\Data_Products\chromedriver.exe')
    driver.get(url)
    delay = 5
    try:
        myElem = WebDriverWait(driver, delay)
        print("Page {} is ready!".format(driver.current_url))
    except TimeoutException:
        print("Loading took too much time!")
    current_page_source = driver.page_source
    soup = BeautifulSoup(current_page_source, 'html.parser')
    try:
        #price = request.html.find('#buyNewSection > div > div > span > span')[0].text
        #price = soup.find('span', {'id': 'newBuyBoxPrice'}).text
        price = soup.find('span', {'class': 'a-size-medium a-color-price offer-price a-text-normal'}).text.strip()
        #price.replace('S$', '').replace(',', '').strip()
    except:
        try:
            price = soup.find('span', {'class': 'a-size-base a-color-price a-color-price'}).text.strip()
        except:
            try:
                price = soup.find('span', {'id': 'price_inside_buybox'}).text.strip()
            except:
                try:
                    price = soup.find('span', {'class': 'a-class-base a-color-secondary'}).text.strip()
                except:    
                    price = None
    try:
        #title = r.html.find('#productTitle')[0].text.strip()
        title = soup.find('span', {'id': 'productTitle'}).text.strip()
    except:
        title = None
    try:
        stock = soup.find('span', {'class': 'a-size-medium a-color-success'}).text.strip()
    except:
        stock = None
    try:
        rating = soup.find('span', {'class': 'a-icon-alt'}).text.strip()
    except:
        rating = None
    try:
        customer_review = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
    except:
        customer_review = None
    try:
        description = soup.find('div', {'id': 'iframeContent'}).text.strip()
    except:
        description = None
    product_dict = {'AsinIsbnRaw': _asin_isbn,
                   'Title': title,
                   'Price': price,
                    'Stock': stock,
                    'Rating': rating,
                    'Customer_Review': customer_review,
                    'Description':  description,
                   'Date': datetime.datetime.now().strftime('%Y-%m-%d'),
                   'Datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    return product_dict


# In[27]:


def amazon_price_list(_asin_isbn_list, _time_sleep = 1):
    
    price_list = []
    
    for item in _asin_isbn_list:
        price_list.append(amazon_price_tracker(item))
        time.sleep(_time_sleep)
        
    return price_list


# In[28]:


def amazon_price_export(price_list, filepath = 'C:\\Users\\65961\\Desktop\\Data_Products\\'):
    
    base = 'webscraping_amazon_price_tracker_v2_'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    extension = '.xlsx'
    filename = filepath + base + timestamp + extension
    
    price_df = pd.DataFrame(price_list)

    price_df['AsinIsbn'] = price_df['AsinIsbnRaw'].apply('="{}"'.format)
        
    price_df.to_excel(filename, index = False)
    
    return price_df


# In[29]:


def amazon_price_pipeline(filename = 'amazon_asin_isbn_20201217.txt', filepath = 'C:\\Users\\65961\\Desktop\\Data_Products\\'):
    
    file = filepath + filename
    with open(file, 'r') as f:
        for line in f:
            _asin_isbn_list = line.split(',')
    
    return amazon_price_export(amazon_price_list(_asin_isbn_list))


# In[30]:


amazon_price_pipeline()


# In[97]:


#asin_isbn_list = ['1118345606', '1591847788', '0470504544', '149207408X', '1119438861', '3319524518', '0062018205', '014311526X']
#asin_isbn_list = ['1118345606', '1591847788', '0470504544']
#with open('amazon_asin_isbn_20201217.csv', 'r') as f:
#    csv_reader = csv.reader(f)
#    for row in csv_reader:
#        row_result = ''
#        row_zero = str(row[0])
#        for character in row_zero:
#            if re.match(pattern, character):
#                row_result = row_result + character
#        asin_isbn_list.append(row_result)


# In[98]:


#pattern = re.compile(r'[a-zA-Z0-9]')


# In[31]:


#if re.match(pattern, asin_isbn_list[0][5]):
#    print('true')

