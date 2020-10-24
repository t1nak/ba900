# ba900

Attention: requires python 2.7! (Yes, the old one, I coded this up a long time ago. So you must create a python environment with python=2.7.; because ``basestring`` is missing in python 3)

# Get the South African Reserve Bank BA 900 forms (time series) 

## Step 1

Run this snippet to create a folder ``data`` in your project directory and one for each year available on the website:

```
import os
folder='data/'
path = os.path.join(os.getcwd(),folder)
years = [i for i in range(2008, 2021, 1)]

for y in years:
    if not os.path.exists(os.path.join(path,str(y))):
        os.makedirs(path+str(y))
```

## Step 2

Download all the xml files from the SARB's [homepage](https://www.resbank.co.za/Research/Statistics/Pages/Banks-BA900-Economic-Returns.aspx) and unzip into the corresponding folder. If I find time I will add a little selenium function to do this automatically, but it's very simple as it is :)

## Step 2

Extract the data from the xml.
Run ```ba900.py``` or the following snipped with the folder name you just created. It will extract all data from the xml files and save as ```year.pkl```. 



```
import pandas as pd 
from collections import Counter
from lxml import etree
import numpy as np
import os, sys
sys.path.insert(0,os.getcwd())
from extract_data import *
from iteration import *
import pickle

folder = os.path.join(os.getcwd(), 'data')

if not os.path.exists(folder): 
    os.mkdir(folder)

years = [ 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

data = save_yearly_data(years, folder)

filename =  os.path.join(folder, 'latest_data.pickle')

with open(filename, 'wb') as f:
    pickle.dump(data, f)

print('All done. Have fun analysing.')

```
