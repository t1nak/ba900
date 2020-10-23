# ba900
Download the South African Reserve Bank BA 900 forms


```
import pandas as pd 
from collections import Counter
from lxml import etree
import numpy as np
import os

import sys
sys.path.insert(0,os.getcwd())
from extract_data import *
from iteration import *
import pickle

folder = os.path.join(os.getcwd(), 'new_data')

if not os.path.exists(folder): 
    os.mkdir(folder)

years = [ 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

data = save_yearly_data(years, folder)

filename =  os.path.join(folder, 'latest_data.pickle')

with open(filename, 'wb') as f:
    pickle.dump(data, f)

print('All done. Have fun analysing.')

```
