#!/usr/bin/env python
# coding: utf-8

# In[57]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime as datetime
import re
import time


# In[58]:


def extract_data(url):
    
    # Define URL
    url = 'https://sg.indeed.com/analytics-jobs-in-Singapore'
    # Launch driver
    driver = webdriver.Chrome()
    # Go to URL
    driver.get(url)
    # Get page source
    pagesource = driver.page_source
    # Create soup
    soup = BeautifulSoup(pagesource, 'html.parser')
    
    # Find job tiles
    tiles = soup.find_all('div', attrs = {'class': 'jobsearch-SerpJobCard unifiedRow row result clickcard'})

    # Find job elements
    item_list = []
    for item in tiles:
        soup_title = item.find('h2', attrs = {'class': 'title'})
        title = soup_title.text.replace('new', '').strip()
        soup_company = item.find('span', attrs = {'class': 'company'})
        company = soup_company.text.strip() 
        soup_summary = item.find('div', attrs = {'class': 'summary'})
        try:
            summary_raw = soup_summary.text.strip()
            pattern = re.compile(r'\n')
            try:
                summary = pattern.sub('. ',summary_raw)
            except:
                summary = summary_raw
        except:
            summary = None
        item_dict = {'JobTitle': title,
                    'Company': company,
                    'Summary': summary,
                    'URL': url,
                    'DatetimeScraped': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        item_list.append(item_dict)
    item_df = pd.DataFrame(item_list)
    
    # Output
    return item_df


# In[59]:


def generate_data(url_main = 'https://sg.indeed.com/jobs?q=analytics&l=Singapore&start=', page_number = 40, export = False):
    
    # Create list to store URLs
    url_list = []
    
    # Create dataframe to store data
    df = pd.DataFrame()
    
    # Generate URLs
    for item in range(1, page_number):
        item_str = str((item - 1)*10)
        url = url_main + item_str
        url_list.append(url)
        item_df = extract_data(url)
        df = pd.concat([df, item_df], axis = 0).reset_index(drop = True)
        time.sleep(3)
        print(f"\nData extracted for URL {url}")
        print(f"Progress: Page {item_str} done")
        
    
    # Remove duplicates
    df = df.drop_duplicates().reset_index(drop = True)
    
    # Show dataframe
    print(f"***Number of rows: {df.shape[0]}\n***Number of columns: {df.shape[1]}")
    print(f"First 5 records:\n{df.head()}")
    
    # Export dataframe
    if export:
        df.to_csv(f"webscraping_indeed_analytics_singapore_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv", index = False)
    
    # Output
    return df, url_list
        


# In[60]:


# Run code
df, url_list = generate_data(export = True)


# In[61]:


df

