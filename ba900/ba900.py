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

data = save_yearly_data(years, input, output)

#This will save all years as one giant pickle (approx. 2GB)
#Uncomment if you want this
# filename =  os.path.join(folder, 'all_data.pickle')
# with open(filename, 'wb') as f:
#     pickle.dump(data, f)

print('All done. Have fun analysing.')
