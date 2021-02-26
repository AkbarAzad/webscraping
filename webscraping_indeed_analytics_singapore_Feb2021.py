#!/usr/bin/env python
# coding: utf-8

# In[114]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime as datetime
import re
import time


# In[119]:


def extract_data(url):
    
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
        try:
            title = soup_title.text.replace('new', '').strip()
        except:
            title = None
        soup_company = item.find('span', attrs = {'class': 'company'})
        try:
            company = soup_company.text.strip()
        except:
            company = None
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


# In[131]:


def generate_data(url_main = 'https://sg.indeed.com/jobs?q=analytics&l=Singapore&start=', page_number = 100, export = False):
    
    # Create list to store URLs
    url_list = []
    
    # Create dataframe to store data
    df = pd.DataFrame()
    
    # Generate URLs
    for item in range(1, (page_number+1)):
        item_str = str((item - 1)*10)
        url = url_main + item_str
        url_list.append(url)
        item_df = extract_data(url)
        df = pd.concat([df, item_df], axis = 0).reset_index(drop = True)
        time.sleep(3)
        print(f"\nData extracted for URL {url}")
        print(f"Progress: Page {str(item)} of {str(page_number)} done")
        
    
    # Remove duplicates
    df = df.drop_duplicates(subset = ['JobTitle','Summary']).reset_index(drop = True)
    
    # Show dataframe
    print(f"***Number of rows: {df.shape[0]}\n***Number of columns: {df.shape[1]}")
    print(f"First 5 records:\n{df.head()}")
    
    # Export dataframe
    if export:
        df.to_csv(f"webscraping_indeed_analytics_singapore_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv", index = False)
    
    # Output
    return df, url_list
        


# In[140]:


# Feature engineering
def feature_engineering(df_raw, export = False):
    
    # Copy dataframe
    df = df_raw.copy()
    
    # If job is an internship, create an is_internship column for df
    df['IsIntern'] = df['JobTitle'].apply(lambda x: 1 if 'intern' in str(x).lower().replace('international', '') else 0)
    
    # If job is in Sales
    df['IsSales'] = df['Summary'].apply(lambda x: 1 if 'sales' in str(x).lower() or 'sell' in str(x).lower() else 0)
    
    # If job is in Marketing
    df['IsMarketing'] = df['Summary'].apply(lambda x: 1 if 'market' in str(x).lower() else 0)
    
    # If job is in Engineering
    df['IsEngineering'] = df['Summary'].apply(lambda x: 1 if 'engineer' in str(x).lower() else 0)
    
    # If job is in Healthcare
    df['IsHealthcare'] = df['Summary'].apply(lambda x: 1 if 'medicine' in str(x).lower() or 'healthcare' in str(x).lower() else 0)
    
    # If job is in Insurance
    df['IsInsurance'] = df['Summary'].apply(lambda x: 1 if 'insurance' in str(x).lower() else 0)
    
    # If job is in Telecommunications
    df['IsTelecommunication'] = df['Summary'].apply(lambda x: 1 if 'telco' in str(x).lower() or 'telecom' in str(x).lower() else 0)
    
    # If job is in Education
    df['IsEducation'] = df['Summary'].apply(lambda x: 1 if 'school' in str(x).lower() or 'student' in str(x).lower() or 'teach' in str(x).lower() else 0)
    
    # If job is in Government-related agencies
    df['IsGovernment'] = df['Summary'].apply(lambda x: 1 if 'government' in str(x).lower() or 'public sector' in str(x).lower() or 'policy' in str(x).lower() else 0)
    
    # If knowledge on data platforms is required
    df['IsTechnology'] = df['Summary'].apply(lambda x: 1 if 'scripting' in str(x).lower() or 'programming' in str(x).lower() or 'languages' in str(x).lower() or 'technolog' in str(x).lower() or 'platform' in str(x).lower() or 'seo' in str(x).lower() else 0)
    
    # If developing models is required
    df['IsModels'] = df['Summary'].apply(lambda x: 1 if 'models' in str(x).lower() or 'operationali' in str(x).lower() or 'deploy' in str(x).lower() else 0)
    
    # If dashboarding or visualisation required
    df['IsVisualisation'] = df['Summary'].apply(lambda x: 1 if 'visuali' in str(x).lower() or 'dashboard' in str(x).lower() or 'story' in str(x).lower() else 0)
    
    # If degree is required
    df['IsDegree'] = df['Summary'].apply(lambda x: 1 if 'degree ' in str(x).lower() or 'bachelor' in str(x).lower() or 'masters' in str(x).lower() or 'phd' in str(x).lower() else 0)
    
    # If experience is required
    df['IsExperience'] = df['Summary'].apply(lambda x: 1 if 'experience' in str(x).lower() else 0)
    
    # Show dataframe
    print(f"***Number of rows: {df.shape[0]}\n***Number of columns: {df.shape[1]}")
    print(f"First 5 records:\n{df.head()}")
    
    # Export as CSV
    if export:
        df.to_csv(f"webscraping_features_indeed_analytics_singapore_{datetime.datetime.now().strftime('%Y%m%d')}.csv", index = False)
    
    # Output
    return df


# In[133]:


# Run code
df, url_list = generate_data(export = True)


# In[141]:


# Feature-enginner dataframe
df_features = feature_engineering(df, export = True)

