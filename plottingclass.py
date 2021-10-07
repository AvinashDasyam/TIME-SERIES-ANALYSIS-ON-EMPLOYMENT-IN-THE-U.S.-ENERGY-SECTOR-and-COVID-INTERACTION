# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 11:23:13 2021

@author: Avinash Dasyam
"""
import pandas
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px


class Plotting:
    
    def covid_vs_all(self,final1):
        ##Monthly covid cases in contrast to all datasets individually
        fig = make_subplots(rows=2, cols=2, subplot_titles =['Covid vs Employement','Covid vs USRigCounts',
                                                              'Covid vs RetailGasolinePrice','Covid vs CrudeOilPrices'])
        fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['EmployedInThousands'], name='EmploymentInThousands'),row=1, col=1)
        fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['USRigCounts'], name='USRigCounts'),row=1, col=2)
        fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['RetailGasolinePrice'], name='RetailGasolinePrice'),row=2, col=1)
        fig.add_trace(go.Scatter(x=final1['Monthly_Covid_cases'], y=final1['CrudeOilPrice'], name='CrudeOilPrice'),row=2, col=2)
        
        fig.update_layout(title_text='<b>Monthly Covidcases in contrast to all Datasets<b>')
        #fig.show()
        #plotly.offline.plot(fig)
        plotly.offline.plot(fig, filename='namefig.html')
        
    def Yearandmonth_multipleaxes(self,final1):


        ##YearandMonth data in contrast to all datasets and multiple Axes
        
        fig1 = go.Figure()
        
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
        fig1.update_layout(title_text='<b>Time Series Correlation<b>')
        plotly.offline.plot(fig1, filename='namefig1.html')
        
    def Correlation_plots(self, final): 
        # MULT Y Employ and Crude Oil Price
        fig2 = make_subplots(specs=[[{'secondary_y': True}]])
        fig2.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name="EmployedInThousands"), secondary_y = False)
        fig2.add_trace(go.Scatter(x = final.YearMonthID, y = final.CrudeOilPrice, name ="CrudeOilPrice"), secondary_y = True)
        fig2.update_yaxes(title_text="Employed (In Thousands) ", secondary_y=False)
        fig2.update_yaxes(title_text="CrudeOilPrice</b> ", secondary_y=True)
        fig2.update_layout(title_text="<b>Correlation of EmployedInThousands and CrudeOilPrice<b>")
        fig2.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig2, filename='namefig2.html')
        
        
        # Multiple Y Employ and Number of Rigs
        fig3 = make_subplots(specs=[[{'secondary_y': True}]])
        fig3.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name="EmployedInThousands"), secondary_y = False)
        fig3.add_trace(go.Scatter(x = final.YearMonthID, y = final.USRigCounts, name ="USRigCounts"), secondary_y = True)
        fig3.update_yaxes(title_text="Employed (In Thousands) ", secondary_y=False)
        fig3.update_yaxes(title_text="USRigCount ", secondary_y=True)
        fig3.update_layout(title_text="<b>Correlation of EmployedInThousands and USRigCounts <b>")
        fig3.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig3, filename='namefig3.html')
           
        # Employment vs Total Renewable Energy
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name="Employed In Thousands"), secondary_y = False)
        fig4.add_trace(go.Scatter(x = final.YearMonthID, y = final.TotalRenewableEnergyProduction, name ="Total Renewable Energy Production"), secondary_y = True)
        fig4.update_yaxes(title_text="Employed (In Thousands) ", secondary_y=False)
        fig4.update_yaxes(title_text="Total Renewable Energy Produced ", secondary_y=True)
        fig4.update_layout(title_text="<b>Correlation of EmployedInThousands and Total Renewable Energy Produced <b>")
        fig4.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig4, filename='namefig4.html')
        
        # correlation of Employement vs Tot Fossil Fuels Produced
        fig5 = make_subplots(specs=[[{'secondary_y': True}]])
        fig5.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name="Employed In Thousands"), secondary_y = False)
        fig5.add_trace(go.Scatter(x = final.YearMonthID, y = final.TotalFossilFuelsProduction, name ="Total Fossil Fuels Production"), secondary_y = True)
        fig5.update_yaxes(title_text="Employed (In Thousands) ", secondary_y=False)
        fig5.update_yaxes(title_text="Total Fossil Fuels Produced ", secondary_y=True)
        fig5.update_layout(title_text="<b>Correlation of EmployedInThousands and Total Fossil Fuels Produced <b>")
        fig5.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig5, filename='namefig5.html')
        
        # correlation of Total Fossil Fuels Production vs Total Renewable Energy Production: 0.627
        fig6 = make_subplots(specs=[[{'secondary_y': True}]])
        fig6.add_trace(go.Scatter(x = final.YearMonthID, y = final.TotalFossilFuelsProduction, name="Total Fossil Fuels Produced"), secondary_y = False)
        fig6.add_trace(go.Scatter(x = final.YearMonthID, y = final.TotalRenewableEnergyProduction, name ="Total Renewable Energy Production"), secondary_y = True)
        fig6.update_yaxes(title_text=" Total Fossil Fuels Produced ", secondary_y=False)
        fig6.update_yaxes(title_text=" Total Renewable Energy Produced ", secondary_y=True)
        fig6.update_layout(title_text="<b>Correlation of Total Fossil Fuels Produced and Total Renewable Energy Produced <b>")
        fig6.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig6, filename='namefig6.html')
           
        
        # Pearsons correlation of monthly_positive_cases vs Employement in oil industry: -0.632
        print("Pearsons correlation of monthly_positive_cases vs Employement in oil industry:", round(final['Monthly_Covid_cases'].corr(final['EmployedInThousands']),3))
        
        fig7 = make_subplots(specs=[[{'secondary_y': True}]])
        fig7.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name="Employed In Thousands"), secondary_y = False)
        fig7.add_trace(go.Scatter(x = final.YearMonthID, y = final.Monthly_Covid_cases, name ="Monthly Covid Cases"), secondary_y = True)
        fig7.update_yaxes(title_text="Employed In Thousands ", secondary_y=False)
        fig7.update_yaxes(title_text="Monthly Covid Cases", secondary_y=True)
        fig7.update_layout(title_text="<b>Correlation of Employed In Thousands and Monthly Covid Cases <b>")
        fig7.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig7, filename='namefig7.html')
   
        
        # Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs: -0.596
        print()
        print("Pearsons correlation of monthly_positive_cases vs Number of U.S Rigs:", round(final['Monthly_Covid_cases'].corr(final['USRigCounts']),3))
        
        fig8 = make_subplots(specs=[[{'secondary_y': True}]])
        fig8.add_trace(go.Scatter(x = final.YearMonthID, y = final.USRigCounts, name="US Rig Count"), secondary_y = False)
        fig8.add_trace(go.Scatter(x = final.YearMonthID, y = final.Monthly_Covid_cases, name ="Monthly Covid Cases"), secondary_y = True)
        fig8.update_yaxes(title_text="US Rig Count ", secondary_y=False)
        fig8.update_yaxes(title_text="Monthly Covid Cases", secondary_y=True)
        fig8.update_layout(title_text="<b>Correlation of US Rig Count and Monthly Covid Cases <b>")
        fig8.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig8, filename='namefig8.html')     
        
        
        # Pearsons correlation of Employement vs Retail Gasoline price: 0.85
        fig9 = make_subplots(specs=[[{'secondary_y': True}]])
        fig9.add_trace(go.Scatter(x = final.YearMonthID, y = final.EmployedInThousands, name = "Employed In Thousands"), secondary_y = False)
        fig9.add_trace(go.Scatter(x = final.YearMonthID, y = final.RetailGasolinePrice, name = "Retail Gasoline Price"), secondary_y = True)
        fig9.update_yaxes(title_text="Employed In Thousands ", secondary_y=False)
        fig9.update_yaxes(title_text="Retail Gasoline Price", secondary_y=True)
        fig9.update_layout(title_text="<b> Correlation of Employed In Thousands and Retail Gasoline Price <b>")
        fig9.update_xaxes(title_text="YearMonthID")
        plotly.offline.plot(fig9, filename='namefig9.html')
    
    def Line_charts(self, final):
         x=final[['EmployedInThousands','USRigCounts','CrudeOilPrice', 'RetailGasolinePrice']]
         x.plot.line(subplots = True, legend = True)
         y=final[['EmployedInThousands','TotalFossilFuelsProduction','TotalRenewableEnergyProduction']]
         y.plot.line(subplots = True, legend = True)
         z=final[['EmployedInThousands','USRigCounts','CrudeOilPrice', 'RetailGasolinePrice', 'Monthly_Covid_cases']]
         z.plot.line(subplots = True, legend = True)
         final.plot.line(subplots = True, legend = False)   
         
     
         
            
            