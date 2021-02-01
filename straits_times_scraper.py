#!/usr/bin/env python
# coding: utf-8

# In[144]:


# Import packages
import requests
import pandas as pd
import datetime
import time
from bs4 import BeautifulSoup
import os
import seaborn as sns
from matplotlib import pyplot as plt


# In[181]:


class straits_times_scraper:
    def __init__(self, url):
        self.url = url
    def extract_headlines(self):
        url_main = self.url
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'From':'https://www.straitstimes.com'}
        response = requests.get(url_main, headers = headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('a')
            item_list = []
            for item in titles:
                try:
                    link = url_main + item['href']
                except:
                    link = None
                title = item.text
                if link is not None and len(title.split()) > 5 and 'javascript:void' not in link.lower():
                    item_dict = {'Title': title,
                                'Link': link,
                                'Datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'Length': len(title),
                                'Category': link.split(sep = "/")[3].strip().lower()}
                    item_list.append(item_dict)
            df = pd.DataFrame(item_list)
            df.to_csv('webscraping_straits_times_news_headlines_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index = False)
            return pd.DataFrame(item_list)
        else:
            print("Response not successful!")
    
    def extract_url(self, category_list = ['Singapore', 'World', 'Asia', 'Opinion', 'Life', 'Business', 'Tech', 'Sport']):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'From':'https://www.straitstimes.com'}
        item_list = []
        for category in category_list:
            url = self.url + '/' + category.lower().strip()
            response = requests.get(url, headers = headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            subcategories = soup.find_all('ul',{'data-parent-menu': category})
            subcategories2 = subcategories[0].text.split(sep = "\n")
            for subcategory in subcategories2:
                item_dict = {'Category': category,
                             'Subcategory': subcategory,
                             'URL': self.url,
                             'URL_Category': url,
                             'URL_Subcategory': url + '/' + subcategory.replace('& ', '').strip().replace(' ', '-').lower()
                
                }
                if len(subcategory) > 0:
                    item_list.append(item_dict)
            print("Category {} links extracted successfully.".format(category))
            time.sleep(5)
        df = pd.DataFrame(item_list)
        df.to_csv('webscraping_straits_times_links_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index = False)
        return df
    
    def extract_titles(self):
        df = self.extract_url()
        title_list = []
        for url in df['URL_Subcategory']:
            response = requests.get(url, headers = headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('span', {'class':'story-headline'})
            for title in titles:
                title_dict = {'URL_Subcategory': url,
                             'Title': title.text.replace("/n", "").strip(),
                              'Datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                             }
                title_list.append(title_dict)
            print("Titles for {} extracted successfully".format(url))
            time.sleep(3)
        title_df = pd.DataFrame(title_list)
        df_merge = pd.merge(title_df, df, how = 'inner', on = ['URL_Subcategory'])
        df_merge = df_merge.reset_index(drop = True)
        df_merge.to_csv('webscraping_straits_times_titles_links_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index = False)
        return df_merge


# In[ ]:


# Compile
def headlines_compiler():
    onlyfiles = [f for f in os.listdir() if 'webscraping_straits_times_news_headlines_' in f and '.csv' in f]
    df = pd.DataFrame()
    for f in onlyfiles:
        try:
            df_f = pd.read_csv(f)
            print('File {} loaded successfully.'.format(f))
        except:
            print('File {} not loaded successfully'.format(f))
            pass
        df = pd.concat([df, df_f], axis = 0)
        df = df.drop_duplicates(subset = ['Title'])
        df = df.reset_index(drop = True)
    df.to_csv('webscraping_compiled_straits_times_news_headlines_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index = False)
    return df


# In[ ]:


# Compile
def news_compiler():
    onlyfiles = [f for f in os.listdir() if 'webscraping_straits_times_titles_links_' in f and '.csv' in f]
    df = pd.DataFrame()
    for f in onlyfiles:
        try:
            df_f = pd.read_csv(f)
            print('File {} loaded successfully.'.format(f))
        except:
            print('File {} not loaded successfully'.format(f))
            pass
        df = pd.concat([df, df_f], axis = 0)
        df = df.drop_duplicates(subset = ['Title'])
        df = df.reset_index(drop = True)
    df['Length'] = df['Title'].apply(len)
    compiled_df = df
    compiled_df.to_csv('webscraping_compiled_straits_times_titles_links_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index = False)
    return compiled_df


# In[ ]:


def plot_histogram(compiled_df, bins = 30):
    min_date = datetime.datetime.strptime(compiled_df['Datetime'].min(), '%Y-%m-%d %H:%M:%S').date().strftime('%d-%b-%Y')
    max_date = datetime.datetime.strptime(compiled_df['Datetime'].max(), '%Y-%m-%d %H:%M:%S').date().strftime('%d-%b-%Y')
    fig, ax = plt.subplots(figsize = (15, 10))
    histogram = compiled_df['Length'].plot(kind = 'hist', bins = bins)
    plt.title("Histogram for Length of News Articles' Titles from Singapore's Straits Times from {} to {}".format(min_date, max_date))
    plt.savefig('webscraping_histogram_compiled_straits_times_titles_links_{}.png'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    plt.show(histogram)
    


# In[ ]:


def plot_boxplot(compiled_df, x = 'Category'):
    min_date = datetime.datetime.strptime(compiled_df['Datetime'].min(), '%Y-%m-%d %H:%M:%S').date().strftime('%d-%b-%Y')
    max_date = datetime.datetime.strptime(compiled_df['Datetime'].max(), '%Y-%m-%d %H:%M:%S').date().strftime('%d-%b-%Y')
    fig, ax = plt.subplots(figsize = (15, 10))
    boxplot = sns.boxplot(ax = ax, data = title_df, x = x, y = 'Length')
    plt.title("Boxplot of Length of News Articles' Titles from Singapore's Straits Times from {} to {}".format(min_date, max_date))
    plt.savefig('webscraping_boxplot_compiled_straits_times_titles_links_{}.png'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    plt.show(boxplot)

    


# In[182]:


bot = straits_times_scraper(url = 'https://www.straitstimes.com')


# In[183]:


df = bot.extract_titles()


# In[208]:


compiled_df = news_compiler()


# In[211]:


plot_histogram(compiled_df)


# In[212]:


plot_boxplot(compiled_df)

