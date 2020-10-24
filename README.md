# ba900

Attention: requires **python 2.7!** Yes, the old one. I coded this up a long time ago.
I will probably transcribe it to python 3 at some point. So long, you must create a python environment with python=2.7 because ``basestring`` is missing in python 3. 

# Get the South African Reserve Bank BA 900 forms -
## Time series of SA banks' balance sheets items 


I provide the data as of 24 October 2020 in this repo.
If you want to update and download yourself, use the following steps.

## Step 1

Run this snippet to create the folder ``data/downloaded`` in your project directory and one for each year available on the website:

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

## Step 3

To convert the data from xml to dataframe
run ```python ba900.py``` or the following snipped with the folder name you just created. The script will extract all data from the xml files and save as ```year.pkl```. 


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

input = os.path.join(os.getcwd(), 'data/downloaded/')
output = os.path.join(os.getcwd(), 'data/output/')

if not os.path.exists(input): 
    os.mkdir(input)

if not os.path.exists(output): 
    os.mkdir(output)

years = [ 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

data = save_yearly_data(years, folder)

#This will save all years as one giant pickle (approx. 2GB)
#Uncomment if you want this
# filename =  os.path.join(folder, 'all_data.pickle')
# with open(filename, 'wb') as f:
#     pickle.dump(data, f)

print('All done. Have fun analysing.')nt('All done. Have fun analysing.')

```
After calling ba900.py you should see something like this:
![image](https://github.com/t1nak/ba900/blob/main/data/success_screenshot.png?raw=true =100x20)

So the banks and their respective monthly data are being processed.
It takes about 30 to 40 min to run all the bank and years (2008 to 2020).

## Step 4

Now you have the data - great. However, analysis of the data requires good understanding of the ba900 forms. 
[Here](https://github.com/t1nak/ba900/blob/main/BA900-2008-12-31.csv) is a csv for ABSA, December 2008.
- [download link](https://raw.githubusercontent.com/t1nak/ba900/main/BA900-2008-12-31.csv) 

There are ``18 tables`` and ``383 unique Item numbers``. For example asset side positions are item numbers ``103`` to ``277``.


After familiarising with the structure, you can load the pickled data and look at the time series with something like this


```

```

Write me if you have questions. There is a lot of 
scope to make this more user-friendly and if I get more feedback I will gladly do so. However, for my own purposes it has been sufficient like it is. 
