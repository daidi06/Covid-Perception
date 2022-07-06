#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np


# In[31]:


import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import unicodedata
import string
import os
import glob
string.punctuation


# # Using `https://allafrica.com/`

# In[32]:


files = glob.glob(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\*')
for f in files:
    os.remove(f)


# # TOPIC 1 : Vaccination

# In[6]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_vac.csv', 
                   sep='\t', 
                   encoding='iso-8859-1')


# In[7]:


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


# In[8]:


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
        globals()["data_vac_" + code] = dtCountry
    else:
        globals()["data_vac_" + code] = pd.DataFrame()


# In[9]:


dataSet = [data_vac_ALG,data_vac_AGO,data_vac_BEN,data_vac_BWA,data_vac_BFA,data_vac_BDI,data_vac_CMR,
          data_vac_CPV,data_vac_CAF,data_vac_TCD,data_vac_COM,data_vac_COG,data_vac_CIV,data_vac_DRC,
          data_vac_GNQ,data_vac_ERI,data_vac_ETH,data_vac_GAB,data_vac_GMB,data_vac_GHA,data_vac_GIN,
          data_vac_GNB,data_vac_KEN,data_vac_LSO,data_vac_LBR,data_vac_MDG,data_vac_MWI,data_vac_MLI,
          data_vac_MRT,data_vac_MUS,data_vac_MOZ,data_vac_NAM,data_vac_NER,data_vac_NGA,data_vac_RWA,
          data_vac_STP,data_vac_SEN,data_vac_SYC,data_vac_SLE,data_vac_ZAF,data_vac_NAM,data_vac_SSD,
          data_vac_SZ,data_vac_TGO,data_vac_UGA,data_vac_TZA,data_vac_ZMB,data_vac_ZW]


# #### Cleaning Content

# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[13]:


filePath = r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\vaccination.csv'

if os.path.exists(filePath):
    os.remove(filePath)


# In[14]:


with open(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\vaccination.csv','a') as f:
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


# In[22]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\vaccination.csv', 
                   sep=',', 
                   encoding='iso-8859-1')


# In[23]:


data = data.reset_index()
data = data.set_axis(['Col_0','Col_1', 'Col_2', 'Col_3','Col_4'], axis='columns')
data.drop('Col_0',axis=1, inplace=True)
#data.head()


# In[24]:


data.drop_duplicates(keep=False, inplace=True, ignore_index=True)
#data.head()


# In[25]:


data.rename(columns={'Col_1':'Sentiment', 'Col_2':'Counts', 
                     'Col_3':'Percentage', 'Col_4':'Countries'}, inplace = True)


# In[26]:


Table_counts = pd.pivot_table(data, values = 'Counts', 
                              index=['Countries'], columns = ['Sentiment'])
#Table_counts


# In[27]:


Table_percentage = pd.pivot_table(data, values = 'Percentage', 
                                  index=['Countries'], columns = ['Sentiment'])
#Table_percentage


# In[28]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\Vaccination_counts.xlsx',engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_counts.to_excel(writer,sheet_name='Counts',startrow=0 , startcol=0)   
writer.save()


# In[29]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\Vaccination_percentage.xlsx',engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_percentage.to_excel(writer,sheet_name='Percentage',startrow=0 , startcol=0)   
writer.save()


# In[ ]:




