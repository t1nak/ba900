#function to convert assets to portfolio weights

def get_pf_weights_by_bank_29(df2):  
    
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
    if df2.iloc[0:2,-29:].sum(axis=1).values[0] == df2[(df2['ItemNumber']=='102')&(df2['ColumnCode']=='1')].Value.values[0]:
        print("CHECKS OUT GREAT! Total assets",df2.iloc[0:2,-29:].sum(axis=1).values[0],df2['InstitutionDescription'].unique(),df2['TheMonth'].unique() ,df2['TheYear'].unique() )

    # df2.iloc[:,-29:]
    total=df2.iloc[0:2,-29:].sum(axis=1).values[0]
    asset_shares_absa = df2.iloc[:,-29:].divide(total , axis=0 )
    df2.iloc[:,-29:] = asset_shares_absa #?
    
    return df2
