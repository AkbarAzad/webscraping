#!/usr/bin/env python
# coding: utf-8

# # Project Yahoo Finance Currency Tracker
# # Akbar Azad

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import time
import os


# In[4]:


def extract_currency(url = 'https://finance.yahoo.com/currencies/'):

    # Extract html from URL
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    # Extract information by ID in multiples of 14 starting from 40 till 390
    id_number = 40
    currency_list = []

    while id_number <= 390:
        id_number_string = str(id_number)
        currency_id = soup.find_all('tr', {'data-reactid':id_number_string})
        #print(len(currency_id))
        currency_info = [f for f in currency_id[0]]
        currency_info_text = [f.text for f in currency_info]
        currency_dict = {'Symbol': currency_info_text[0],
                        'Name': currency_info_text[1],
                        'Last_Price': currency_info_text[2],
                        'Change': currency_info_text[3],
                        '%_Change': currency_info_text[4]}
        currency_list.append(currency_dict)
        if currency_info_text[2] == "-":
            id_number += 12
        else:
            id_number += 14
    
    currency_df = pd.DataFrame(currency_list)
    
    currency_df.to_csv('C:\\Users\\65961\\OneDrive\\Desktop\\Data_Products\\' + 'webscraping_yahoo_finance_currency_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', index = False)
    
    return currency_df


# In[5]:


currency_df = extract_currency()

