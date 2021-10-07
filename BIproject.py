
import pandas as pd
import numpy as np
import datetime
import seaborn as sn
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from plottingclass import Plotting

################### DATASETS ###############################
############################################################
path =  'C:/Users/14699/TSA_of_Covid_impacting_others/'
file1 = 'Employed.csv'
file2 = 'WTI Cruide Oil Price.csv'
file3 = 'Worldwide Rig Count Aug 2021.csv'
file4 = 'Table_1.2_Primary_Energy_Production_by_Source.csv'
file5 = 'PET_PRI_GND_DCUS_NUS_W.csv'
file6 = 'us_covid19_daily.csv'

emp = pd.read_csv(path + file1, skiprows = 16)
crude = pd.read_csv(path + file2)
rigc = pd.read_csv(path + file3)
energy = pd.read_csv(path + file4,skiprows=9)
retail = pd.read_csv(path + file5)
covid = pd.read_csv(path + file6)


'''Crude Dataset'''
#############################################################
# dropping unnecessary rows from header
crude.drop(crude.index[[0,1]], axis=0, inplace=True)
# check columns
crude.columns
#Rename column
crude.rename(columns = {'Back to Contents': 'year_month', 'Data 1: Cushing, OK WTI Spot Price FOB (Dollars per Barrel)': 'WTI_price'}, inplace = True)
crude.columns
#converting year_months to id format to merge
crude['year_month'] = pd.to_datetime(crude['year_month']).dt.strftime('%Y%m')


'''Energy Dataset'''
##############################################################
#setting appropiate column  name from csv file row.
energy.columns = energy.iloc[0]
#dropping unnecessary rows from dataframe
energy.drop(energy.index[0:2], axis=0, inplace=True)
#setting year_month id
energy['year_month'] = pd.to_datetime(energy['Month']).dt.strftime('%Y%m')
energy = energy[['year_month','Total Fossil Fuels Production', 'Total Renewable Energy Production']]


'''Rigs Dataset'''
##############################################################
rigc.rename(columns=lambda x: x.strip())
rigc['Month_ID'] = 0
rigc['Month_ID']= pd.to_numeric(rigc['Month_ID'])
def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1
for i,v in rigc['Month'].iteritems():
    rigc.at[i,'Month_ID'] =  int(month_converter(v))   
rigc['year_month'] = rigc['Year'].astype(str) + rigc['Month_ID'].astype(str).str.zfill(2)
rigDF = rigc[['year_month','Month','Year','U.S']]

'''Covid Dataset'''
##############################################################
covid = covid[['date','positive']]
covid['positive_cases'] = covid['positive']
covid['positive_cases'] = covid['positive_cases'].shift(1)
covid['daily_positive_cases'] = covid['positive_cases'] - covid['positive']
covid = covid.drop(columns = ['positive_cases','positive'])
covid = covid.shift(-1)
covid = covid.drop([0,319])
covid.index = pd.to_datetime(covid['date'], format = '%Y%m%d', errors = 'ignore')
covid = covid.drop(columns = ['date'])
covid = covid.groupby(pd.Grouper(freq='M')).sum()
covid = covid.rename(columns ={'daily_positive_cases':'monthly_positive_cases'} )
covid = covid.reset_index()
covid['year_month'] = covid['date'].dt.strftime('%Y%m')
covid = covid.drop(columns = ['date'])


'''Employement dataset'''
################################################################
emp.columns = emp.iloc[0]
emp = emp[['Label','Observation Value']]
emp.drop(emp.index[0], axis=0, inplace=True)
emp = emp.reset_index()
emp = emp.drop(columns = ['index'])
emp['year_month'] = pd.to_datetime(emp['Label']).dt.strftime('%Y%m')
#emp['year_month'] = emp['Label'].apply( lambda x: datetime.strptime(x, '%Y %b')\.strftime('%Y%m') )
emp = emp.drop(columns = ['Label'])


'''Retail Petrol price'''
################################################################
#WE WILL USE R3 WHICH IS REFORMULATED REGULAR GASOLINE TO ABIDE BY 1990 CLEAN AIR ACT
# df.drop(columns=['B', 'C'])
retail = retail.drop(columns = ['A1','A2','A3','R1','R2','M1','M2',
                                      'M3','P1','P2','P3','D1'])  
# want data starting at Janurary 2010
# row 782 is last data of 2009
# final_retail = retail.drop(retail.loc([0:782]))
# drop through January 2010
retail = retail.drop(retail.index[0:783])
# drop through May 2021
# "%m/%d/%y"
retail['Year'] = pd.to_datetime(retail['Date']).dt.year
retail['Month'] = pd.to_datetime(retail['Date']).dt.month
retail['year_month'] = retail['Year'].astype(str) +  + retail['Month'].astype(str).str.zfill(2)
retail = retail.sort_values(by='year_month')
retail = retail[['year_month','R3']].groupby(['year_month']).mean()
retail = pd.DataFrame(retail)
retail = retail.reset_index()
# to manually add the missing data in from eia.gov
dic = {'year_month': ['202102','202103','202104','202105'],
       'R3': ['2.69400','2.99700','3.04800','3.20200']}
new_data = pd.DataFrame(dic)
retail = retail.append(new_data, ignore_index = True)


################# Merging all the dataframes ####################
#################################################################
final = pd.merge(emp, crude, how = 'inner', on = 'year_month')
final = pd.merge(final, rigDF, how = 'inner', on = 'year_month')
final = pd.merge(final, energy, how = 'inner', on = 'year_month')
final = pd.merge(final, retail, how = 'inner', on = 'year_month')
final = pd.merge(final, covid, how = 'left', left_on = 'year_month', right_on = 'year_month')

final.columns
final.drop(final.index[0:2], axis=0, inplace=True)
final = final[['year_month', 'Observation Value', 'WTI_price', 'U.S', 'Total Fossil Fuels Production','Total Renewable Energy Production','R3', 'monthly_positive_cases']]


############## Converting variables to numeric ##################
#################################################################
final['Observation Value']=pd.to_numeric(final['Observation Value'])
final['R3']=pd.to_numeric(final['R3'])
final['U.S']=pd.to_numeric(final['U.S'])
final['monthly_positive_cases']=pd.to_numeric(final['monthly_positive_cases'])
final['WTI_price']=pd.to_numeric(final['WTI_price'])
final['Total Fossil Fuels Production']=pd.to_numeric(final['Total Fossil Fuels Production'])
final['Total Renewable Energy Production']=pd.to_numeric(final['Total Renewable Energy Production'])


################### Finding Correlation ##########################
##################################################################
print("Pearsons correlation of Employement vs Number of U.S Rigs:", round(final['U.S'].corr(final['Observation Value']),3))

print("Pearsons correlation of Employement vs Crude oil price:", round(final['U.S'].corr(final['WTI_price']),3))

print("Pearsons correlation of Employement vs Total Renewable Energy Production:", round(final['U.S'].corr(final['Total Renewable Energy Production']),3))

print("Pearsons correlation of Employement vs Retail Gasoline price:", round(final['U.S'].corr(final['R3']),3))

print("Pearsons correlation of Total Fossil Fuels Production vs Total Renewable Energy Production:", round(final['Total Fossil Fuels Production'].corr(final['Total Renewable Energy Production']),3))

print("Pearsons correlation of monthly_positive_cases vs Employement in oil industry:", round(final['monthly_positive_cases'].corr(final['Observation Value']),3))

print("Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs:", round(final['monthly_positive_cases'].corr(final['U.S']),3))
# Pearsons correlation of Employement vs Number of U.S Rigs: 0.717
# Pearsons correlation of Employement vs Crude oil price: 0.879
# Pearsons correlation of Employement vs Total Renewable Energy Production: -0.653
# Pearsons correlation of Employement vs Retail Gasoline price: 0.85
# Pearsons correlation of Total Fossil Fuels Production vs Total Renewable Energy Production: 0.627
# Pearsons correlation of monthly_positive_cases vs Employement in oil industry: -0.632
# Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs: -0.596



#################### Renaming all column names ##################
#################################################################
final.rename(columns = {'year_month':'YearMonthID', 'Observation Value': 'EmployedInThousands', 'WTI_price':'CrudeOilPrice', 'U.S':'USRigCounts','R3':'RetailGasolinePrice','monthly_positive_cases':'Monthly_Covid_cases'
                        ,'Total Fossil Fuels Production':'TotalFossilFuelsProduction','Total Renewable Energy Production':'TotalRenewableEnergyProduction'}, inplace = True)

########### Creating Correlation Matrix with Heatmap ############
#################################################################
corrMatrix = final.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()


############ Duplicating the Final dataset ######################
final1 = final.copy()

###### Dropping the corresponsding NULL values handling #########
#################################################################
#Dropping null values of covid cases starting from 2012 to 2019
final1.dropna(subset = ['Monthly_Covid_cases'],inplace=True)

#########  #Creating object(instance) for plotting class ########
obj1_plotting = Plotting()

##Monthly covid cases in contrast to all datasets individually
obj1_plotting.covid_vs_all(final1)

##YearandMonth data in contrast to all datasets and multiple Axes
obj1_plotting.Yearandmonth_multipleaxes(final1)

##individual Correlation
obj1_plotting.Correlation_plots(final)

            
obj1_plotting.Line_charts(final)