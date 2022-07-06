#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np


# In[12]:


import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import unicodedata
import string
import os
import glob
string.punctuation


# # Using `https://allafrica.com/`

# # TOPIC 3 : Non-Pharmaceutical measures

# In[13]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_NPMeasures.csv', 
                   sep='\t', 
                   encoding='iso-8859-1')


# In[14]:


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


# In[15]:


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
        globals()["data_NPMeasures_" + code] = dtCountry
    else:
        globals()["data_NPMeasures_" + code] = pd.DataFrame()


# In[16]:


dataSet = [data_NPMeasures_ALG,data_NPMeasures_AGO,data_NPMeasures_BEN,data_NPMeasures_BWA,data_NPMeasures_BFA,data_NPMeasures_BDI,data_NPMeasures_CMR,
          data_NPMeasures_CPV,data_NPMeasures_CAF,data_NPMeasures_TCD,data_NPMeasures_COM,data_NPMeasures_COG,data_NPMeasures_CIV,data_NPMeasures_DRC,
          data_NPMeasures_GNQ,data_NPMeasures_ERI,data_NPMeasures_ETH,data_NPMeasures_GAB,data_NPMeasures_GMB,data_NPMeasures_GHA,data_NPMeasures_GIN,
          data_NPMeasures_GNB,data_NPMeasures_KEN,data_NPMeasures_LSO,data_NPMeasures_LBR,data_NPMeasures_MDG,data_NPMeasures_MWI,data_NPMeasures_MLI,
          data_NPMeasures_MRT,data_NPMeasures_MUS,data_NPMeasures_MOZ,data_NPMeasures_NAM,data_NPMeasures_NER,data_NPMeasures_NGA,data_NPMeasures_RWA,
          data_NPMeasures_STP,data_NPMeasures_SEN,data_NPMeasures_SYC,data_NPMeasures_SLE,data_NPMeasures_ZAF,data_NPMeasures_NAM,data_NPMeasures_SSD,
          data_NPMeasures_SZ,data_NPMeasures_TGO,data_NPMeasures_UGA,data_NPMeasures_TZA,data_NPMeasures_ZMB,data_NPMeasures_ZW]


# #### Cleaning Content

# In[17]:


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


# In[18]:


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


# In[19]:


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


# In[20]:


filePath = r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\NonPharmaceuticalMeasures.csv'

if os.path.exists(filePath):
    os.remove(filePath)


# In[21]:


with open(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\NonPharmaceuticalMeasures.csv','a') as f:
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


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\NonPharmaceuticalMeasures.csv', 
                   sep=',', 
                   encoding='iso-8859-1')
#data.head()


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


#data.head()


# In[27]:


Table_counts = pd.pivot_table(data, values = 'Counts', 
                              index=['Countries'], columns = ['Sentiment'])
#Table_counts.head()


# In[28]:


Table_percentage = pd.pivot_table(data, values = 'Percentage', 
                                  index=['Countries'], columns = ['Sentiment'])
#Table_percentage.head()


# In[29]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\NonPharmaceuticalMeasures_counts.xlsx',
                        engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_counts.to_excel(writer, sheet_name='Counts', startrow=0 , startcol=0)   
writer.save()


# In[30]:


writer = pd.ExcelWriter(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Output\NonPharmaceuticalMeasures_percentage.xlsx',
                        engine='xlsxwriter')   # Creating Excel Writer Object from Pandas  
Table_percentage.to_excel(writer, sheet_name='Percentage', startrow=0 , startcol=0)   
writer.save()


# In[ ]:





# In[ ]:




