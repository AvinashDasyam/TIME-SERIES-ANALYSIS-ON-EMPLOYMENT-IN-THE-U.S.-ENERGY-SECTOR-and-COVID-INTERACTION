
import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
import seaborn as sn
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from django.shortcuts import render

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


'''crude'''
# dropping unnecessary rows from header
crude.drop(crude.index[[0,1]], axis=0, inplace=True)
# check columns
crude.columns
#Rename column
crude.rename(columns = {'Back to Contents': 'year_month', 'Data 1: Cushing, OK WTI Spot Price FOB (Dollars per Barrel)': 'WTI_price'}, inplace = True)
crude.columns
#converting year_months to id format to merge
crude['year_month'] = pd.to_datetime(crude['year_month']).dt.strftime('%Y%m')


'''energy'''
#setting appropiate column  name from csv file row.
energy.columns = energy.iloc[0]
#dropping unnecessary rows from dataframe

energy.drop(energy.index[0:2], axis=0, inplace=True)
#setting year_month id
energy['year_month'] = pd.to_datetime(energy['Month']).dt.strftime('%Y%m')
energy = energy[['year_month','Total Fossil Fuels Production', 'Total Renewable Energy Production']]


'''rigc'''
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




'''covid'''
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


'''emp'''
emp.columns = emp.iloc[0]
emp = emp[['Label','Observation Value']]
emp.drop(emp.index[0], axis=0, inplace=True)
emp = emp.reset_index()
emp = emp.drop(columns = ['index'])
emp['year_month'] = pd.to_datetime(emp['Label']).dt.strftime('%Y%m')
#emp['year_month'] = emp['Label'].apply( lambda x: datetime.strptime(x, '%Y %b')\.strftime('%Y%m') )
emp = emp.drop(columns = ['Label'])


'''retail'''
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
# df['yr'] = pd.to_datetime([df['birthdate']).dt.year()
retail['Year'] = pd.to_datetime(retail['Date']).dt.year
retail['Month'] = pd.to_datetime(retail['Date']).dt.month
retail['year_month'] = retail['Year'].astype(str) +  + retail['Month'].astype(str).str.zfill(2)

retail = retail.sort_values(by='year_month')


#retail_avgs = final_retail[['Date', 'R3']].groupby(['Date']).mean()
retail = retail[['year_month','R3']].groupby(['year_month']).mean()

retail = pd.DataFrame(retail)
retail = retail.reset_index()

# to manually add the missing data in from eia.gov
dic = {'year_month': ['202102','202103','202104','202105'],
       'R3': ['2.69400','2.99700','3.04800','3.20200']}

new_data = pd.DataFrame(dic)

retail = retail.append(new_data, ignore_index = True)


#Merging all the dataframe

final = pd.merge(emp, crude, how = 'inner', on = 'year_month')
final = pd.merge(final, rigDF, how = 'inner', on = 'year_month')
final = pd.merge(final, energy, how = 'inner', on = 'year_month')
final = pd.merge(final, retail, how = 'inner', on = 'year_month')
final = pd.merge(final, covid, how = 'left', left_on = 'year_month', right_on = 'year_month')

final.columns
final.drop(final.index[0:2], axis=0, inplace=True)
final = final[['year_month', 'Observation Value', 'WTI_price', 'U.S', 'Total Fossil Fuels Production','Total Renewable Energy Production','R3', 'monthly_positive_cases']]

# Pearson's correlation
#rigc=rigc.rename(columns={'Observation Value': 'Employement(in thousands)'})
final['Observation Value']=pd.to_numeric(final['Observation Value'])

rigc=rigc.rename(columns={'Observation Value': 'Employement(in thousands)'})
final['Observation Value']=pd.to_numeric(final['Observation Value'])
print("Pearsons correlation of Employement vs Number of U.S Rigs:", round(final['U.S'].corr(final['Observation Value']),3))

final['WTI_price']=pd.to_numeric(final['WTI_price'])
print("Pearsons correlation of Employement vs Crude oil price:", round(final['U.S'].corr(final['WTI_price']),3))

final['Total Renewable Energy Production']=pd.to_numeric(final['Total Renewable Energy Production'])
print("Pearsons correlation of Employement vs Total Renewable Energy Production:", round(final['U.S'].corr(final['Total Renewable Energy Production']),3))


final['R3']=pd.to_numeric(final['R3'])
print("Pearsons correlation of Employement vs Retail Gasoline price:", round(final['U.S'].corr(final['R3']),3))

final['Total Fossil Fuels Production']=pd.to_numeric(final['Total Fossil Fuels Production'])
final['Total Renewable Energy Production']=pd.to_numeric(final['Total Renewable Energy Production'])
print("Pearsons correlation of Total Fossil Fuels Production vs Total Renewable Energy Production:", round(final['Total Fossil Fuels Production'].corr(final['Total Renewable Energy Production']),3))

final['monthly_positive_cases']=pd.to_numeric(final['monthly_positive_cases'])
print("Pearsons correlation of monthly_positive_cases vs Employement in oil industry:", round(final['monthly_positive_cases'].corr(final['Observation Value']),3))

final['U.S']=pd.to_numeric(final['U.S'])
print("Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs:", round(final['monthly_positive_cases'].corr(final['U.S']),3))


final.rename(columns = {'year_month':'YearMonthID', 'Observation Value': 'EmployedInThousands', 'WTI_price':'CrudeOilPrice', 'U.S':'USRigCounts','R3':'RetailGasolinePrice','monthly_positive_cases':'Monthly_Covid_cases'}, inplace = True)


corrMatrix = final.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()

# Pearsons correlation of Employement vs Number of U.S Rigs: 0.717
# Pearsons correlation of Employement vs Crude oil price: 0.879
# Pearsons correlation of Employement vs Total Renewable Energy Production: -0.653
# Pearsons correlation of Employement vs Retail Gasoline price: 0.85
# Pearsons correlation of Total Fossil Fuels Production vs Total Renewable Energy Production: 0.627
# Pearsons correlation of monthly_positive_cases vs Employement in oil industry: -0.632
# Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs: -0.596


final1 = final
#dropping null values of covid cases starting from 2012 to 2019
final1.dropna(subset = ['Monthly_Covid_cases'],inplace=True)

##Monthly covid cases in contrast to all datasets individually
fig = make_subplots(rows=2, cols=2, subplot_titles =['Covid vs Employement','Covid vs USRigCounts',
                                                      'Covid vs RetailGasolinePrice','Covid vs CrudeOilPrices'])
fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['EmployedInThousands'], name='EmploymentInThousands'),row=1, col=1)
fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['USRigCounts'], name='USRigCounts'),row=1, col=2)
fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['RetailGasolinePrice'], name='RetailGasolinePrice'),row=2, col=1)
fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['CrudeOilPrice'], name='CrudeOilPrice'),row=2, col=2)

fig.update_layout(title_text='Monthly Covidcases in contrast to all Datasets')
#fig.show()
#plotly.offline.plot(fig)

##YearandMonth data in contrast to all datasets and multiple Axes

fig1 = go.Figure()


#final1['YearMonthID'] = pd.to_numeric(final1['YearMonthID'])

fig1.add_trace(go.Scatter(x=final1['YearMonthID'],y=final1['Monthly_Covid_cases'],name="Monthly_Covid_cases"))
fig1.add_trace(go.Scatter(x=final1['YearMonthID'],y=final1['EmployedInThousands'],name="EmployedInThousands",yaxis="y2"))
fig1.add_trace(go.Scatter(x=final1['YearMonthID'],y=final1['USRigCounts'],name="USRigCounts",yaxis="y3"))
fig1.add_trace(go.Scatter(x=final1['YearMonthID'],y=final1['RetailGasolinePrice'],name="RetailGasolinePrice",yaxis="y4"))

# Create axis objects
fig1.update_layout(xaxis=dict(domain=[0.3, 0.7]
    ),
    yaxis=dict(
        title="Monthly_Covid_cases",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
    ),
    yaxis2=dict(
        title="EmployedInThousands",
        titlefont=dict(
            color="#ff7f0e"
        ),
        tickfont=dict(
            color="#ff7f0e"
        ),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.15
    ),
    yaxis3=dict(
        title="USRigCounts",
        titlefont=dict(
            color="#d62728"
        ),
        tickfont=dict(
            color="#d62728"
        ),
        anchor="x",
        overlaying="y",
        side="right"
    ),
    yaxis4=dict(
        title="RetailGasolinePrice",
        titlefont=dict(
            color="#9467bd"
        ),
        tickfont=dict(
            color="#9467bd"
        ),
        anchor="free",
        overlaying="y",
        side="right",
        position=0.85
    )
   
)

# Update layout properties
fig1.update_layout(title_text='Time Series Correlation')
#fig1.show()
#plotly.offline.plot(fig1)

#regressor = LinearRegression()


#print('Drafted')
# plotly.offline.plot(fig, filename='name.html')
# plotly.offline.plot(fig1, filename='name.html')

with open('p_graph.html', 'a') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    #f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))


plt_div = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
