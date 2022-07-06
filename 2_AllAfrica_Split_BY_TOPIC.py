#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# # Using `https://allafrica.com/`

# In[3]:


data = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\dataFrom_allafrica_COVID_all_last.csv', sep='\t', encoding='iso-8859-1')


# # TOPIC 1 : Vaccination

'''
`Keywords` : First dose, second dose, covid 19, COVID19, COVID-19, SARS-CoV-2, corona virus, covid jab, 
Pfizer, astra, astrazeneca, covax, moderna, sinovac, sinopharm side effects, covid 5G, antivax, priority groups
'''
# 

# In[19]:


keywords = ['First dose', 'second dose', 'covid 19', 'COVID19', 'COVID-19', 'SARS-CoV-2', 'corona virus', 
            'covid jab', 'Pfizer', 'astra', 'astrazeneca', 'covax', 'moderna', 'sinovac', 'sinopharm side effects', 
            'covid 5G', 'antivax', 'priority groups']


# In[20]:


data['TitleL'] = data['Title'].str.lower()
data['StorieL'] = data['Storie'].str.lower()
data_vac = pd.DataFrame()
for kw in keywords:
    kw = kw.lower()
    dtCountry = data[(data['StorieL'].str.contains(kw)) | (data['TitleL'].str.contains(kw))]
    if (len(dtCountry)>0):
        data_vac = pd.concat([data_vac, dtCountry], ignore_index=False)
data_vac.drop_duplicates(keep = 'first', inplace = True)


# In[21]:


# # TOPIC 2 : Case management

'''
`Keywords` : frontline workers, ICU, oxygen, quarantine, fly and test, drug authority, ICU beds, face masks, 
protective equipment, PPE, immunity, covid recovery, covid deaths, critical condition, sanitizer, hospitalization, 
self isolation, temperature, ventilators, pcr, rapid test, covid-19 treatment, immunity boost, booster
'''

# In[23]:


keywords = ['frontline workers', 'ICU', 'oxygen', 'quarantine', 'fly and test', 'drug authority', 
            'ICU beds', 'face masks', 'protective equipment', 'PPE', 'immunity', 'covid recovery', 
            'covid deaths', 'critical condition', 'sanitizer', 'hospitalization', 'self isolation', 
            'temperature', 'ventilators', 'pcr', 'rapid test', 'covid-19 treatment', 'immunity boost', 
            'booster']


# In[24]:


data['TitleL'] = data['Title'].str.lower()
data['StorieL'] = data['Storie'].str.lower()
data_caseM = pd.DataFrame()
for kw in keywords:
    kw = kw.lower()
    dtCountry = data[(data['StorieL'].str.contains(kw)) | (data['TitleL'].str.contains(kw))]
    if (len(dtCountry)>0):
        data_caseM = pd.concat([data_caseM, dtCountry], ignore_index=False)
data_caseM.drop_duplicates(keep = 'first', inplace = True)


# In[25]:



# # TOPIC 3 : Non-Pharmaceutical measures

'''
`Keywords` : COVID, Pandemic, hand washing, lockdown, quarantine, curfew, social distancing, temperature, teleworking, 
closure of schools, mask, Suspension of Religious activities, Suspension of Domestic travels, 
Total refusal of entry for all foreign nationals, Closure of restaurants and bars, Refusal for high risk countries, 
Visa Refusal, Suspension of sporting activities, gathering restriction
'''

# In[27]:


keywords = ['Pandemic', 'hand washing', 'lockdown', 'quarantine', 'curfew', 'social distancing', 
            'temperature', 'teleworking', 'closure of schools', 'mask', 'Suspension of Religious activities', 
            'Suspension of Domestic travels', 'Total refusal of entry for all foreign nationals', 
            'Closure of restaurants and bars', 'Refusal for high risk countries', 'Visa Refusal', 
            'Suspension of sporting activities', 'gathering restriction']


# In[28]:


data['TitleL'] = data['Title'].str.lower()
data['StorieL'] = data['Storie'].str.lower()
data_NPMeasures = pd.DataFrame()
for kw in keywords:
    kw = kw.lower()
    dtCountry = data[(data['StorieL'].str.contains(kw)) | (data['TitleL'].str.contains(kw))]
    if (len(dtCountry)>0):
        data_NPMeasures = pd.concat([data_NPMeasures, dtCountry], ignore_index=False)
data_NPMeasures.drop_duplicates(keep = 'first', inplace = True)


# In[31]:


data_vac.to_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_vac.csv', sep = '\t', index=False)


# In[32]:


data_caseM.to_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_caseM.csv', sep = '\t', index=False)


# In[33]:


data_NPMeasures.to_csv(r'D:\PERSONNEL\OMS\TRAVAIL\COVID\Demo\Files\data_NPMeasures.csv', sep = '\t', index=False)



