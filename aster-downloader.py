#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import osmnx as ox
import pandas as pd
import requests
import shutil
from keys import username, password, urls_path, dl_folder

timeout = 30


# In[ ]:


assert os.path.isfile(urls_path)
if not os.path.exists(dl_folder):
    os.makedirs(dl_folder)


# In[ ]:


def login(url):
    session = requests.session()
    session.auth = (username, password)
    redirect = session.get(url, timeout=timeout)
    response = session.get(redirect.url, timeout=timeout)
    assert response.ok
    print(ox.ts(), 'status', response.status_code, 'logged in')
    return session


# In[ ]:


def download_file(url, session, filepath):
    try:
        with session.get(url, stream=True, timeout=timeout) as response:
            assert response.ok
            with open(filepath, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
                print(ox.ts(), 'status', response.status_code, 'saved', filepath)
    except Exception as e:
        print(ox.ts(), e)


# In[ ]:


def get_filepath(url):
    return os.path.join(dl_folder, url.split('/')[-1])


# In[ ]:


urls = pd.read_csv(urls_path, header=None).iloc[:,0].sort_values()
print(ox.ts(), 'there are', len(urls), 'urls to get')

session = login(urls[0])

for url in urls:
    filepath = get_filepath(url)
    if os.path.isfile(filepath):
        print(ox.ts(), filepath, 'already exists')
    else:
        download_file(url, session, filepath)
        
session.close()
print(ox.ts(), 'finished', len(urls), 'urls ->', len(os.listdir(dl_folder)), 'files')


# In[ ]:




