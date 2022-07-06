#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from time import sleep
import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
from bs4 import BeautifulSoup
import pickle


# # Using `https://allafrica.com/`

# In[2]:


# get the last page number
url = 'https://allafrica.com/search/index.html?search_string=covid&search_submit=Search&page=1'
page= requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
list_last_page=soup.find('li', {'class': 'last'})
page_url = list_last_page.find('a')
lastPage_url_href = page_url.get('href')
last_number = lastPage_url_href.split('page=')[-1]
last_number = int(last_number) + 1

def allUrl(num):
    u = "https://allafrica.com/search/index.html?search_string=covid&search_submit=Search&page="
    num=str(num)
    u=u+num
    return u

all_urls = list(map(allUrl, range(1, last_number)))


# In[3]:


#To read it back:
with open ('D:\\PERSONNEL\\OMS\\TRAVAIL\\COVID\\Demo\\Files\\clean_result', 'rb') as fp:
    clean_result = pickle.load(fp)


# In[4]:


baseURL= 'https://allafrica.com'
StorieTitle = []
StorieText = []
StorieNotDownload = []

gateway = ApiGateway("https://allafrica.com", 
                     access_key_id='AKIAXOSLUJ5C4KYXUO4P', 
                     access_key_secret='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')
gateway.start()

session = requests.Session()
session.mount("https://allafrica.com", gateway)

result=[]

for url in all_urls:
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    leader_board=soup.find(class_="stories")
    players = leader_board.find_all('a', href=True)
    player_name = [player['href']for player in players]
    clean_player_name = [s for s in player_name if "/stories/" in s]
    new_player_name = list(set(clean_player_name) - set(clean_result))
    if len(new_player_name) :
        result.extend(new_player_name)
    else:
        break
    

for link in result:
    gobalLink = baseURL+link
    try:
        storiePage = session.get(gobalLink)
        soup = BeautifulSoup(storiePage.content, 'html.parser')
        titre=soup.find(class_="headline").get_text()
        Pstories=soup.find_all(class_="story-body-text")
        storie = ' '.join([paragraph.get_text() for paragraph in Pstories])
        StorieTitle.append(titre)
        StorieText.append(storie)
    except requests.ConnectionError as e:
        StorieNotDownload.append(link)
        sleep(10)
        gateway.shutdown() # Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.
        gateway = ApiGateway("https://allafrica.com", 
                     access_key_id='AKIAXOSLUJ5C4KYXUO4P', 
                     access_key_secret='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')
        gateway.start()
        session = requests.Session()
        session.mount("https://allafrica.com", gateway)
        continue
    except requests.Timeout as e:
        StorieNotDownload.append(link)
        sleep(10)
        gateway.shutdown() # Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.
        gateway = ApiGateway("https://allafrica.com", 
                     access_key_id='AKIAXOSLUJ5C4KYXUO4P', 
                     access_key_secret='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')
        gateway.start()
        session = requests.Session()
        session.mount("https://allafrica.com", gateway)
        continue
    except requests.RequestException as e:
        StorieNotDownload.append(link)
        sleep(10)
        gateway.shutdown() # Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.
        gateway = ApiGateway("https://allafrica.com", 
                     access_key_id='AKIAXOSLUJ5C4KYXUO4P', 
                     access_key_secret='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')
        gateway.start()
        session = requests.Session()
        session.mount("https://allafrica.com", gateway)
        continue
    
gateway.shutdown()


# In[5]:


if len(StorieNotDownload):
    baseURL= 'https://allafrica.com'
    gateway = ApiGateway("https://allafrica.com", 
                         access_key_id='AKIAXOSLUJ5C4KYXUO4P', 
                         access_key_secret='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')
    gateway.start()
    session = requests.Session()
    session.mount("https://allafrica.com", gateway)
    for link in StorieNotDownload:
        gobalLink = baseURL+link
        storiePage = session.get(gobalLink)
        soup = BeautifulSoup(storiePage.content, 'html.parser')
        titre=soup.find(class_="headline").get_text()
        Pstories=soup.find_all(class_="story-body-text")
        storie = ' '.join([paragraph.get_text() for paragraph in Pstories])
        StorieTitle.append(titre)
        StorieText.append(storie)
        sleep(50)
    gateway.shutdown()


# In[6]:


newData = pd.DataFrame({'Title':StorieTitle, 'Storie':StorieText, 'link':result})


# In[7]:


newData.to_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\dataFrom_allafrica_COVID_all_Update.csv', sep = '\t', index=False)


# In[8]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\dataFrom_allafrica_COVID_all_last.csv', sep = '\t', encoding='iso-8859-1')
#data.shape


# In[9]:


dataUpdate = pd.concat([data, newData], ignore_index=True)
#data.append(newData, ignore_index=True)
#dataUpdate.shape


# In[10]:


dataUpdate.to_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\dataFrom_allafrica_COVID_all_last.csv', sep = '\t', index=False)


# In[11]:


clean_result.extend(result)

with open('D:\\PERSONNEL\\OMS\\TRAVAIL\\COVID\\Files\\clean_result', 'wb') as fp:
    pickle.dump(clean_result, fp)


# In[ ]:




