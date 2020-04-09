#!/usr/bin/env python
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-reader
# ****

# In[3]:


import pandas as pd


# ## imports for Python, Pandas

# In[6]:


import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas.pydata.org/pandas-docs/stable/io.html#normalization

# In[4]:


# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[7]:


# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[8]:


# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 

# In[25]:


# load json as string
json.load((open('data/world_bank_projects.json')))


# In[245]:


# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects.json')
sample_json_df[['countryname','project_name']].head()


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[267]:


import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
#Load data
data = json.load(open( 'data/world_bank_projects.json'))


# In[449]:


#Create dataframe from JSON_data
df1 = json_normalize(data)
#Count the countrynames to get the number of projects
top_10_projects = df1['countryname'].value_counts()
top_10_projects.head(10)


# In[450]:


#Create new dataframe to find the themes
df2 = json_normalize(data, 'mjtheme_namecode')
#Count the theme
top_10_themes = df2['name'].value_counts()
top_10_themes.head(10)


# In[451]:


#Check the kind of data the empty values are, instead of null values, they are empty strings
df2.iloc[1]


# In[452]:


#Count the number of empty values there are
df2[df2['name'] == ''].count()


# In[456]:


#Convert empty strings to nulls
df2.replace(to_replace = '', value = np.nan, inplace = True)


# In[457]:


#Create new dataframe with missing values
df3 = df2.dropna(axis=0)
df3.drop_duplicates(inplace=True)


# In[458]:


df3.shape


# In[459]:


#Create dictionary to create key-value pairs to iterate over Q2's dataframe's empty values
code_dict = dict(zip(df3['code'].values, df3['name'].values))


# In[460]:


df2['name'] = df2['name'].fillna(df2.code.map(code_dict))
df2['name'].value_counts().head(10)


# In[461]:


#Check blanks
df2[pd.isnull(df2['name'])].count()

