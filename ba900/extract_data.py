from more_itertools import unique_everseen
from collections import Counter
from lxml import etree
import pandas as pd
import numpy as np
from iteration import *
import os

def save_yearly_data(years, dirin, dirout):

	all_data = []
	for y in years:
		paths = []
		rootdir = dirin+str(y)+'/'
		print(rootdir)
		for subdir_month, dirs, files in os.walk(rootdir):
			paths.append(subdir_month)


		year = min(paths, key=len)
		paths.remove(year)
		monthly_data = []
		list_keys = []

		for path in paths:
			if path != year:
				print(path)
				monthly = get_all_monthly_data(path)
				monthly_data.append(monthly)
				list_keys.append(path[-13:-6])
		# df_Master = pd.concat(monthly_data, keys=list_keys)

		df_Master = pd.concat(monthly_data)
		df_Master.to_pickle(dirout+"/df"+str(y)+".pkl")
		print("Yearly data was written in" ,dirout,"df",str(y),".pkl")
		all_data.append(df_Master)
	return all_data



def get_all_monthly_data(path):

	time = path[-13:-6]
 
	files = iterate_folder(path)
	banks={}
	df_list= []
	keys_list = []
	for key in files.keys():
		for file in files[key]:
			xml = file
			with open (xml) as fobj:
				xml = fobj.read()
			root = etree.fromstring(xml)

			bank_name, bank = get_bank_data(root)
			# print(bank_name)
			banks[bank_name]=bank
	for k, v in banks.iteritems():
		df_list.append(v)
		keys_list.append(k)
	month = pd.concat(df_list)

	# month = pd.concat(df_list,keys=keys_list)

	month['time'] = time
	print('all monthly data for all banks at time', time, 'was extracted')	
	return month 


def get_bank_data(root):

	keys = []
	df_list = []
	for i in range(19):
		identifier = i+1
		ROWS = get_table_description(root)
		for dic in ROWS:
			if dic['TableNumber']== str(identifier):
				tablenumber = dic['TableNumber'] 
		if  isinstance(tablenumber, basestring):
			df = get_table_data(tablenumber,root)
			print(tablenumber), str(df['InstitutionDescription'].values[0])
			df_list.append(df)
			keys.append(tablenumber)
				# df.to_csv('/Users/Tina/Dropbox/phd/'+ str(identifier) + '.csv')		
		else:
			pass
				 
		# df.to_pickle("/Users/Tina/Dropbox/phd/df.pkl")  
	if len(df_list)>1:
		# df_Master = pd.concat(df_list, keys=keys)
		df_Master = pd.concat(df_list)
		bank_key = str(df_Master['InstitutionDescription'].values[0])
		return str(bank_key), df_Master # df_Master.to_csv('/Users/Tina/Dropbox/phd/alltables.csv') 


def get_table_description(root):

	table_description = []

	for table in root.getchildren():
		for elem in table.getchildren():
			for key,val in elem.attrib.iteritems():
				table_descrip = {}
				if key=="TableDescription" or key=="TableNumber":
					table_descrip[key]=val
					table_description.append(table_descrip)

	ROWS = []
	rows = list(zip(table_description[::2], table_description[1::2]))

	for i in rows:
		d = {}
		a, b = i
		d.update(a)
		d.update(b)
		ROWS.append(d)

	return ROWS



def get_table_data(tablenumber, root):
	rows2=[]
	rows3 = []
	items = []

	values = []
	which_bank = []
 
	for t in root.iter():
		if t.tag=='SARBForms':
			which_bank.append(t.attrib)

	for t in root.getchildren():
		for elem in t.getchildren():
			for key,val in elem.attrib.iteritems():
				if val == tablenumber:
				# if val==table[0][key] and len(table[0][key])<=2:
				  
					for item in elem.getchildren():
						for key2, value2 in item.attrib.iteritems():
							# print key2, value2 
							if key2=='ColumnDescription':
								all2 = {}
								all2[key2]=value2
								rows2.append(all2)
								break
						for key2, value2 in item.attrib.iteritems():
							# print key2, value2 
							if key2=='ColumnCode':
								col3 = {}
								col3[key2]=value2
								rows3.append(col3)
								break

						for i, ii in zip(rows2, rows3):
							for k,v in ii.iteritems():
								i[k] = v

						for value in item.getchildren():
							for i in item.attrib:
								if i == 'ItemNumber':
									itemnumber = item.attrib[i]
									x={i:item.attrib[i]}
									y=value.attrib,  x
									values.append(y)
									break	 
						tempd = {}
						for l, item in item.attrib.iteritems():
					 		if l=="ItemNumber" or l=="ItemDescription":
					 			tempd[l] = item
					 			items.append(tempd)
					break

	all_val = []		
	for i in values:
		d = {}
		a, b  = i
		d[a.keys()[0]]=a[a.keys()[0]]
		d[a.keys()[1]]=a[a.keys()[1]]
		d.update(b)
		all_val.append(d)
 	

	total = []
	count =0
	for i in items:
	 	i2 = dict(i)

	 	for ro in rows2:
	 		t = ro, i2
	 		total.append(t)
	 		count+=1
	

	total = list(unique_everseen(total))

	TOT = []
	for i in total:
		d = {}
		a, b = i
		d.update(a)
		d.update(b)
		TOT.append(d)
	for i in TOT:
		for ii in all_val:
			if i['ItemNumber'] ==ii['ItemNumber']:
				if "000"+i['ColumnCode']==ii['ColumnNumber']:
					i['Value']= ii['Value']
					break


	temp=pd.DataFrame(TOT)

	temp['TableNumber']=tablenumber

	for i in which_bank:
		for key in i.keys():
			temp[key]=i[key]

	return temp 



def get_path(root):
	from lxml import etree
	parser = etree.XMLParser(recover=True)
	tree = etree.ElementTree(root)

	for tag in root.iter():
	    path = tree.getpath(tag)
	    print(path)
	    # print root.xpath("SARBForms/SARBForm/Table[1]/ColumnHeader[1]")

def get_individual_table(id, root, output_path):
	df = get_table_data(str(id),root)
	# df.to_csv(output_path+ str(id) + '.csv')
	# print 'output generated in', output_path
	return df	 
 
