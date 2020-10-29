#function to convert assets to portfolio weights
import pandas as pd
import numpy as np

class tranformer():

	def __init__(self):
		pass



	def get_bank_totals(self, id, bankstring,jahr, monat, dfrenamed):
	    helper={}

	    month=monat
	    year=jahr


	    b=bankstring

	    helper['id']=id
	    helper['name']=b
	    helper['equity']=self.get_equity_single_value(b, month,year,  dfrenamed )*1000
	    helper['year']=year
	    helper['month'] = month
	    helper['debt']=self.get_debt_single_value(b, month,year, dfrenamed )*1000
	    helper['leverage']=self.get_debt_single_value(b, month,year, dfrenamed )/self.get_equity_single_value(b, month,year,  dfrenamed )
	    helper['total_assets']=self.get_total_assets_single_value(b, month,year, dfrenamed )*1000

	    #get the weights - call function and select single value and last 29 columns to get only the weights
	    test=self.get_bankdata_29assets([year],[month],dfrenamed, b)
	    # # we only need one entry per month - so select column code 7 and itemnumber 2 for example 
	    test_weights=test[(test['ColumnCode']=='7')&(test['ItemNumber']=='2')]
	    test_weights.index=test_weights.time
	    weights_only=test_weights[test_weights.columns[-29:]] 

	    helper['time']=test_weights.time
	    for column in weights_only:
	        helper[column]=weights_only[column][-1]

	    if helper['total_assets']==(helper['equity']+ helper['debt']):
	        df4=pd.DataFrame(helper)

	        # Check constitency ==1?
	        if round(df4.iloc[0:1,-29:].sum(axis=1).values[0])==1:
	            # print(b,'returned')
	            return df4
		            
	def get_overview_timeseries(self,banklist, months,years,dfrenamed):
	    import string
	    letters = list(string.ascii_uppercase)[:26]

	    temp1=[]
	    temp2=[]
	    temp3=[]
	    for y in years:
	        for m in months:
	            # Get bank totals for each of those strings 
	            for name,l in zip(banklist,letters):
	                temp1.append(self.get_bank_totals(l,name,y, m, dfrenamed))

	            temp2.append(pd.concat(temp1))
	        temp3.append(pd.concat(temp2))
	    df=pd.concat(temp3)
	    df=df.drop_duplicates()
	    return df


	def get_weights_banks_timeseries_29assets(self, years, months, alldata, banklist):
		dicp={}
		for jahr in years:

			for month in months:
				df2=pd.DataFrame()
				for b in banklist:
					try:
						test=self.get_bankdata_29assets([jahr],[month],alldata, b)
						test_weights=test[(test['ColumnCode']=='7')&(test['ItemNumber']=='2')]
						test_weights.index=test_weights.time
						weights_only=test_weights[test_weights.columns[-29:]] 
						#build for all banks, but one time
						df2[b] = weights_only.T[weights_only.T.columns[0]]
						k=weights_only.T.columns[0]
					except:
						print(b,'did not work')

				dicp[k]=df2
			print(jahr, ' processed')
		return dicp 

	def get_pf_weights_by_bank_29(self,df2):  
	    names_group1=['South_African_bank_notes_and_subsidiary_coin',
	                  'Gold_coin_and_bullion',
	                  'Domestic_currency_deposits_with_SA_Reserve_Bank',
	                  "SA_Interbank",
	                  "Rand_Deposits_to_and_loans_to_foreign_banks",
	                  "Loans_granted_under_repo_agreement",
	                  "Foreign_currency_loans_and_advances",
	                  "Redeemable_preference_shares",
	    #               
	                  'Corporate_installments',
	                  'Household_installments',
	                  'Corporate_mortgages',\
	                  'Household_mortgages',\
	                 'Corporate_credit_card',\
	                  'Household_credit_card',\
	                   'Corporate_leasing',\
	                  'Household_leasing',\
	                  'Corporate_unsecured_lending',\
	                  'Household_unsecured_lending',\
	                  'Other_credit',
	    #              
	                   'Central_and_provincial_government_bonds',\
	                    'Other_public_sector_bonds',\
	                    'Private_sector_bonds',\
	                  'Equity_holdings_in_subsidiaries_and_joint_ventures',\
	                    'Listed_and_unlisted_equities',
	                  'Securitisation/ asset-backed_securities',\
	                'Derivative_instruments',\
	                'Treasury_bills_SA_Reserve_Bank_bills_Land_Bank_bills','Other_investments_less_impairments','Non_financial_assets']  
	    #                 'impairments'

	    t=[   [104,'positive'],\
	         [105,'positive'],\
	          [106,'positive'],\
	          [111,'positive'],\
	       [117,'positive'],\
	         [118,'positive'],\
	         [126,'positive'],\
	           [135,'positive'],\
	        ([140,'positive'], [143,'negative']), \
	       [143,'positive'],\
	        ([150,'positive'], [164,153,157,'negative']), \
	         [164,153,157,'positive'] ,\
	       ([166,'positive'], [169,'negative']),\
	          [169,'positive'],\
	        ([145,'positive'], [148,'negative']),\
	          [148,'positive'],\
	       ([188,'positive'], [192,'negative']),\
	        [192,'positive'],\
	       [187,171,181,'positive'],\
	       [196,'positive'],\
	          [207,'positive'],\
	            [213,'positive'],\
	       [221,217 ,'positive'] ,\
	      [225,229 ,'positive'] ,\
	       [233,'positive'],\
	       [237,'positive'],\
	       [251, 252, 254,'positive'] ,\
	       ([241, 246, 'positive'], [ 251,252,254,245,194,'negative']),\
	       [258,267,'positive']]
	    
	    
	    #balance sheet accounting magic 
	    count=1
	    for i, name in zip(t,names_group1):
	        if type(i)==tuple:
	            temp=0
	            for item in i[1][:-1]:#sum of second element
	    #             print(item, df1[(df1['ItemNumber']==str(abs(item)))&(df['ColumnCode']=='5')].Value.values[0])
	                temp+= df2[(df2['ItemNumber']==str(abs(item)))&(df2['ColumnCode']=='5')].Value.values[0]

	            if i[1][-1]=='negative':
	                 temp=-1*temp

	            temp2=0       
	            for item in i[0][:-1]:
	                temp2+= df2[(df2['ItemNumber']==str(abs(item)))&(df2['ColumnCode']=='5')].Value.values[0]
	            if i[0][-1]=='positive':
	                 temp2=1*temp2

	            df2["m{}_{}".format(count,name)] = temp2 + temp

	        if type(i)!=tuple: #if is not a tuple we don't subtrat
	            df2["m{}_{}".format(count,name)]= 0

	            if i[-1]=='positive':
	                for number in i[:-1]:
	                    df2["m{}_{}".format(count,name)]+= df2[(df2['ItemNumber']==str(abs(number)))&(df2['ColumnCode']=='5')].Value.values[0]

	            if i[-1]=='negative':
	                for number in i[:-1]:
	                    df2["m{}_{}".format(count,name)]+= df2[(df2['ItemNumber']==str(abs(number)))&(df2['ColumnCode']=='5')].Value.values[0]
	                df2["m{}_{}".format(count,name)]=-1*df2["m{}_{}".format(count,name)].values
	        count+=1
	          
	    # check consistency
	    # if df2.iloc[0:2,-29:].sum(axis=1).values[0] == df2[(df2['ItemNumber']=='102')&(df2['ColumnCode']=='1')].Value.values[0]:
	    #     print("CHECKS OUT GREAT! Total assets",df2.iloc[0:2,-29:].sum(axis=1).values[0],df2['InstitutionDescription'].unique(),df2['TheMonth'].unique() ,df2['TheYear'].unique() )

	    # df2.iloc[:,-29:]
	    total=df2.iloc[0:2,-29:].sum(axis=1).values[0]
	    asset_shares_absa = df2.iloc[:,-29:].divide(total , axis=0 )
	    df2.iloc[:,-29:] = asset_shares_absa #?
	    # print(df2['InstitutionDescription'].unique()," processed and returned weights")
	    return df2

	def get_bankdata_29assets(self, years,months,df, bank_string):
	    helper_dict={}
	    for y in years:
	        helper_dict[y]=months

	    BANK = df[df['InstitutionDescription']==bank_string]
	    BANK['Value'] = pd.to_numeric(BANK['Value'])

	    bank_year_and_month = []
	    for key in helper_dict.keys():
	        for month in helper_dict[key]:
	            df_bank_key_month =  BANK[(BANK['TheYear']==key)&(BANK['TheMonth']==month)]
	            try:
	                bank_year_and_month.append(self.get_pf_weights_by_bank_29(df_bank_key_month))
	            except:
	                pass

	    bank=pd.concat(bank_year_and_month)
	    # print('all data returned for ',bank_string)
	    return bank

	def relabel_banknames(self, banklistfrom, banklisto,bigdata):
	    
	    for old, new in zip(banklistfrom,banklisto):
	        
	        try:
	            bigdata['InstitutionDescription'] = bigdata['InstitutionDescription'].apply(lambda x: x.replace(old, new))
	            print('changed {} to: {}'.format(old, new))
	        except:
	            print(old,'was not found')
	    return bigdata
	        

	def get_equity_single_value(self, bankstring, monthstring, yearstring , MASTER):
	    
	    try:
	        equity=MASTER[(MASTER['TheYear']==yearstring)&(MASTER['TheMonth']==monthstring)&
	                  (MASTER['InstitutionDescription']==bankstring)&(MASTER['ItemNumber']=='96')&(MASTER['ColumnCode']=='1')]
	        return float(equity.Value.values[0])
	    
	    except:
	        print("did not work - perhaps bank string {} was incorrect?".format(bankstring))
	

	def get_debt_single_value(self, bankstring, monthstring, yearstring , MASTER):
	    
	    try:
	        debt=MASTER[(MASTER['TheYear']==yearstring)&(MASTER['TheMonth']==monthstring)&
	                  (MASTER['InstitutionDescription']==bankstring)&(MASTER['ItemNumber']=='95')&(MASTER['ColumnCode']=='4')]
	        return float(debt.Value.values[0])
	    
	    except:
	        print("did not work - perhaps bank {} string was incorrect?".format(bankstring))

	def get_total_assets_single_value(self, bankstring, monthstring, yearstring , MASTER):
	    
	    try:
	        debt=MASTER[(MASTER['TheYear']==yearstring)&(MASTER['TheMonth']==monthstring)&
	                  (MASTER['InstitutionDescription']==bankstring)&(MASTER['ItemNumber']=='102')&(MASTER['ColumnCode']=='1')]
	        return (debt.Value.values[0])
	    except:
	        print("did not work - perhaps bank {} string was incorrect?".format(bankstring))
	        

	def create_similarity_matrix(self, banklist, dictionary, dictkey):
		#Make filler matrix
		import numpy as np
		filler=pd.DataFrame( columns=banklist, index=banklist)
		t4=filler
		w=dictionary[dictkey]

		for bank1 in banklist:    
			for bank2 in banklist:
				t4.at[bank2, bank1] =np.linalg.norm(w[bank1]-w[bank2])
		return t4

	def get_biggest_banks(self, yearstring, monthstring, bigdata, topnumber):
	    year = yearstring
	    month= monthstring
	    a=bigdata[(bigdata['ColumnCode']=='7')&(bigdata['ItemNumber']=='2')\
	          &(bigdata['TheYear']==yearstring)&(bigdata['TheMonth']==monthstring)
	          ]
	    a['Value'] = pd.to_numeric(a['Value'])
	    sorted=a.sort_values(by='Value', ascending=False)
	    selected=sorted[sorted.InstitutionCode!='TOTAL'].InstitutionDescription.head(topnumber)
	    return selected 
			

