# Importing libraries
import os
import pathlib
import shutil
import pandas as pd
import numpy as np
from scipy import stats
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import datetime
import xlx

# Change to you local directory */
os.chdir('C:\Suvo\PGP-BABI\India Petrol Prices')

# Month Encode function
def encodemonth(c):
    if c == 'January':
        return 1
    if c == 'February':
        return 2    
    if c == 'March':
        return 3
    if c == 'April':
        return 4
    if c == 'May':
        return 5
    if c == 'June':
        return 6
    if c == 'July':
        return 7
    if c == 'August':
        return 8
    if c == 'September':
        return 9
    if c == 'October':
        return 10
    if c == 'November':
        return 11
    if c == 'December':
        return 12
        

# 
# Read live data 
# Online Ref: https://iocl.com/Product_PreviousPrice/PetrolPreviousPriceDynamic.aspx
#
petrolprice = pd.read_excel('Previous Petrol Prices.xlsx',sheetname='Sheet1')

# Parse the date fields
petrolprice['MonthIndex'] = petrolprice.apply(lambda row: datetime.datetime.strptime(row.Month, '%B %d, %Y').strftime('%Y-%m-%d'), axis=1)

# Fetch Delhi prices
petrolprice_Delhi = petrolprice.loc[:,['MonthIndex','Delhi']]
petrolprice_Delhi.index = petrolprice_Delhi.MonthIndex

petrolprice_Delhi = petrolprice_Delhi.loc[:,['Delhi']]
petrolprice_Delhi.head(3)

# Canculate Percentage changes of petrol prices
percentchangeprice_Delhi = petrolprice_Delhi.pct_change()

# fill the missing values with 0 as no price change happened for that day
percentchangeprice_Delhi.fillna(0,inplace=True)

percentchangeprice_Delhi['MonthDate'] = percentchangeprice_Delhi.index

# Derive Month/Year field 
percentchangeprice_Delhi['Month'] = percentchangeprice_Delhi.apply(lambda row: datetime.datetime.strptime(row.MonthDate, '%Y-%m-%d').strftime('%B,%Y'), axis=1)

# Agreegate prices over each month/year
meanpercentchangeprice_Delhi = pd.DataFrame(percentchangeprice_Delhi.groupby(percentchangeprice_Delhi['Month']).agg({'Delhi': 'mean'}))

meanpercentchangeprice_Delhi['MonthYear'] = meanpercentchangeprice_Delhi.index

# Extract Month and Year component
meanpercentchangeprice_Delhi['Year'] = meanpercentchangeprice_Delhi.apply(lambda row: row.MonthYear.split(',')[1], axis=1)
meanpercentchangeprice_Delhi['Month'] = meanpercentchangeprice_Delhi.apply(lambda row: row.MonthYear.split(',')[0], axis=1)

# Encode months
meanpercentchangeprice_Delhi['EncodeMonth'] = meanpercentchangeprice_Delhi['Month'].apply(encodemonth)

# Sort the data in proper order and store in a final dataframe
finalpricechange = pd.DataFrame(meanpercentchangeprice_Delhi.sort_values(by=['Year','EncodeMonth']))

# 
# Plot the Delhi price changes over months
# Range: June, 2002 - May, 2018
#
finalpricechange.Delhi.plot(kind='line')

#g = sns.barplot(finalpricechange.MonthYear, finalpricechange.Delhi)

# 
# Different plots using seaborn library
# 

# Box - Plot
g = sns.boxplot(finalpricechange.Year, finalpricechange.Delhi)
g.set_xticklabels(g.get_xticklabels(),rotation='vertical')

# Bar - Plot
g = sns.barplot(finalpricechange.Year, finalpricechange.Delhi)
g.set_xticklabels(g.get_xticklabels(),rotation='vertical')