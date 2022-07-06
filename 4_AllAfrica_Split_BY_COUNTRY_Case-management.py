#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import unicodedata
import string
import os
import glob
string.punctuation


# # Using `https://allafrica.com/`

# # TOPIC 2 : Case management

# In[3]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_caseM.csv', 
                   sep='\t', 
                   encoding='iso-8859-1')


# In[4]:


Countries=['ALGERIA', 'ANGOLA', 'BENIN', 'BOTSWANA',
       'BURKINA FASO', 'BURUNDI', 'CAMEROON', 'CABO VERDE',
       'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'COMOROS', 'REPUBLIC OF CONGO',
       "CÔTE D'IVOIRE", 'DEMOCRATIC REPUBLIC OF CONGO',
       'EQUATORIAL GUINEA', 'ERITREA', 'ETHIOPIA', 'GABON', 'GAMBIA',
       'GHANA', 'GUINEA', 'GUINEA-BISSAU', 'KENYA', 'LESOTHO', 'LIBERIA',
       'MADAGASCAR', 'MALAWI', 'MALI', 'MAURITANIA', 'MAURITIUS',
       'MOZAMBIQUE', 'NAMIBIA', 'NIGER', 'NIGERIA', 'RWANDA',
       'SÃO TOMÉ AND PRÍNCIPE', 'SENEGAL', 'SEYCHELLES', 'SIERRA LEONE',
       'SOUTH AFRICA', 'SOUTH SUDAN', 'ESWATINI', 'TOGO', 'UGANDA',
       'UNITED REPUBLIC OF TANZANIA', 'ZAMBIA', 'ZIMBABWE']
CountryCode=['ALG', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV',
            'CAF', 'TCD', 'COM', 'COG', 'CIV', 'DRC', 'GNQ', 'ERI',
            'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 
            'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MOZ', 'NAM',
            'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'ZAF',
            'SSD', 'SZ', 'TGO', 'UGA', 'TZA', 'ZMB', 'ZW']


# In[5]:


data['TitleL'] = data['Title'].str.lower()
data['StorieL'] = data['Storie'].str.lower()
CountryWithData = []
CountryWithDataIndex = []
CountryWithDatalen = []
for country, code, i in zip(Countries, CountryCode, range(len(Countries))):
    country = country.lower()
    dtCountry = data[(data['StorieL'].str.contains(country)) | (data['TitleL'].str.contains(country))]
    if (len(dtCountry)>0):
        CountryWithData.append(Countries[i])
        CountryWithDataIndex.append(i)
        CountryWithDatalen.append(len(dtCountry))
        globals()["data_caseM_" + code] = dtCountry
    else:
        globals()["data_caseM_" + code] = pd.DataFrame()


# In[6]:


dataSet = [data_caseM_ALG,data_caseM_AGO,data_caseM_BEN,data_caseM_BWA,data_caseM_BFA,data_caseM_BDI,data_caseM_CMR,
          data_caseM_CPV,data_caseM_CAF,data_caseM_TCD,data_caseM_COM,data_caseM_COG,data_caseM_CIV,data_caseM_DRC,
          data_caseM_GNQ,data_caseM_ERI,data_caseM_ETH,data_caseM_GAB,data_caseM_GMB,data_caseM_GHA,data_caseM_GIN,
          data_caseM_GNB,data_caseM_KEN,data_caseM_LSO,data_caseM_LBR,data_caseM_MDG,data_caseM_MWI,data_caseM_MLI,
          data_caseM_MRT,data_caseM_MUS,data_caseM_MOZ,data_caseM_NAM,data_caseM_NER,data_caseM_NGA,data_caseM_RWA,
          data_caseM_STP,data_caseM_SEN,data_caseM_SYC,data_caseM_SLE,data_caseM_ZAF,data_caseM_NAM,data_caseM_SSD,
          data_caseM_SZ,data_caseM_TGO,data_caseM_UGA,data_caseM_TZA,data_caseM_ZMB,data_caseM_ZW]


# #### Cleaning Content

# In[7]:


#Remove Punctuation
def remove_punct(txt):
    txt  = "".join([char for char in txt if char not in string.punctuation])    
    txt1 = re.sub('[0-9]+', '', txt)
    #remove mentions@
    txt1 = re.sub(r'@[A-Za-z0-9_]+', '', txt1)
    # Remove hashtags
    txt1 = re.sub(r'#', '', txt1)
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    no_url = url_pattern.sub(r'', txt1)
    text = (unicodedata.normalize('NFKD', no_url).encode('ascii', 'ignore').decode('utf-8', 'ignore'))
    return text


# In[8]:


def SentimentAnalysisCountry(data, var, threshold):
    
    sid = SIA()
    data['sentiments'] = data[var].apply(lambda x: sid.polarity_scores(' '.join(re.findall(r'\w+',x))))

    # Obtaining NLTK compound score
    data['nltk_cmp_score'] = data['sentiments'].apply(lambda score_dict: score_dict['compound'])


    data['Positive Sentiment'] = data['sentiments'].apply(lambda x: x['pos']+1*(10**-6)) 
    data['Neutral Sentiment'] = data['sentiments'].apply(lambda x: x['neu']+1*(10**-6))
    data['Negative Sentiment'] = data['sentiments'].apply(lambda x: x['neg']+1*(10**-6))
    
    neutral_thresh = threshold
    
    # Categorize scores into the sentiments of positive, neutral or negative using compund
    data['nltk_sentiment'] = data['nltk_cmp_score'].apply(lambda c: 'Positive' if c >= neutral_thresh else ('Negative' if c <= -(neutral_thresh) else 'Neutral'))
    return data


# In[9]:


# Define function to get value counts
def get_value_counts(data, col_name, countrie):
    count = pd.DataFrame(data[col_name].value_counts())
    percentage = pd.DataFrame(data[col_name].value_counts(normalize=True).mul(100))
    value_counts_df = pd.concat([count, percentage], axis = 1)
    value_counts_df = value_counts_df.reset_index()
    value_counts_df.columns = ['sentiment', 'counts', 'percentage']
    value_counts_df.sort_values('sentiment', inplace = True)
    value_counts_df['percentage'] = value_counts_df['percentage'].apply(lambda x: round(x,2))
    value_counts_df['Countrie'] = countrie
    value_counts_df = value_counts_df.reset_index(drop = True)
    return value_counts_df


# In[10]:


filePath = r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\caseManagement.csv'

if os.path.exists(filePath):
    os.remove(filePath)


# In[11]:


with open(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\caseManagement.csv','a') as f:
    for countrie, code, dt in zip(Countries, CountryCode, dataSet):
        try:
            data = dt.copy()
            data["Content"] = data[['Title', 'Storie']].apply(lambda x: ' '.join(x), axis=1)
            data = data[data.Storie.notna()]
            data = data[data.Content.notna()]
            data['Content_punct'] = data['Content'].apply(lambda x:remove_punct(x.lower()))
            data_final = SentimentAnalysisCountry(data, 'Content_punct', 0.05)
            nltk_sentiment_df = get_value_counts(data_final, 'nltk_sentiment', code)
            f.write(f'Countrie: {countrie}')
            f.write("\n")
            nltk_sentiment_df.to_csv(f)
            f.write("\n")
        except:
            f.write(f'Countrie: {countrie}')
            f.write("\n")
            f.write("\n")


# In[12]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\caseManagement.csv', 
                   sep=',', 
                   encoding='iso-8859-1')
#data.head()


# In[13]:


data = data.reset_index()
data = data.set_axis(['Col_0','Col_1', 'Col_2', 'Col_3','Col_4'], axis='columns')
data.drop('Col_0',axis=1, inplace=True)
#data.head()


# In[14]:


data.drop_duplicates(keep=False, inplace=True, ignore_index=True)
#data.head()


# In[15]:


data.rename(columns={'Col_1':'Sentiment', 'Col_2':'Counts', 
                     'Col_3':'Percentage', 'Col_4':'Countries'}, inplace = True)


# In[16]:


#data.head()


# In[17]:


Table_counts = pd.pivot_table(data, values = 'Counts', 
                              index=['Countries'], columns = ['Sentiment'])
#Table_counts.head()


# In[18]:


Table_percentage = pd.pivot_table(data, values = 'Percentage', 
                                  index=['Countries'], columns = ['Sentiment'])
#Table_percentage.head()


# In[19]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\caseManagement_counts.xlsx',engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_counts.to_excel(writer,sheet_name='Counts',startrow=0 , startcol=0)   
writer.save()


# In[20]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\caseManagement_percentage.xlsx',engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_percentage.to_excel(writer,sheet_name='Percentage',startrow=0 , startcol=0)   
writer.save()

