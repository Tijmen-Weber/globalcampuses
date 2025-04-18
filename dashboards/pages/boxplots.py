
#Packages
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

df = pd.read_excel('Total Data nov 2021.xlsx')
dfLME = df[df['VoC']=='LME']
dfCME = df[df['VoC']=='CME']
dfSME = df[df['VoC']=='SME']

#Defining the app
dash.register_page(__name__)

layout = html.Div([
    html.H2("Spending on Higher Education and International Students"),#title
    dcc.RadioItems(#radioitems
        id='radioitems',
        options=[
            {'label':'Public Spending on Higher Education','value':'PubSpGDP'},#label is the name in the dropdown, value is the name of the column in the data
            {'label':'Private Spending on Higher Education','value':'PrivSpGDP'},
            {'label':'Percentage International Students','value':'IntRatioNonEU'}],
        value='PubSpGDP',
        style={'display':'flex','flex-direction':'column','font-family':'sans-serif'}),
    html.Div([#first row
        html.Div(dcc.Graph(id='All',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}),style={'padding':1}),
        html.Div(dcc.Graph(id='LME',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}),style={'padding':1})],
        style={'display':'flex','flex-direction':'row'}),
    html.Div([#second row
        html.Div(dcc.Graph(id='CME',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}),style={'padding':1}),
        html.Div(dcc.Graph(id='SME',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}),style={'padding':1})],
        style={'display':'flex','flex-direction':'row'})
    ],
    style={'font-family':'sans-serif'})

@callback(
    Output("All", "figure"),
    Output("LME", "figure"),
    Output("CME", "figure"),
    Output("SME", "figure"),
    Input("radioitems", "value")
    )

def update_graphs(y):
    range_y_dict = {'PubSpGDP': (0, 2), 'PrivSpGDP': (0, 2), 'IntRatioNonEU': (0, 25)} #change y=axis ranges
    range_y = range_y_dict.get(y)

    figall = px.box(df, x='Year',y=y,range_y=range_y,title='All Countries',
                    labels = {'PubSpGDP': 'Public Spending as a % of GDP',
                              'PrivSpGDP': 'Private Spending as a % of GDP',
                              'IntRatioNonEU': 'Percentage International Students'})
    figall.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 400,width=400)
    figall.update_traces(marker_color='#5D6D7E')

    figLME = px.box(dfLME, x='Year',y=y,range_y=range_y,title='Liberal Market Economies',
                    labels = {'PubSpGDP': 'Public Spending as a % of GDP',
                              'PrivSpGDP': 'Private Spending as a % of GDP',
                              'IntRatioNonEU': 'Percentage International Students'})
    figLME.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 400,width=400)
    figLME.update_traces(marker_color='#FBA72A')

    figCME = px.box(dfCME, x='Year',y=y,range_y=range_y,title='Coordinated Market Economies',
                    labels = {'PubSpGDP': 'Public Spending as a % of GDP',
                              'PrivSpGDP': 'Private Spending as a % of GDP',
                              'IntRatioNonEU': 'Percentage International Students'})
    figCME.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 400,width=400)
    figCME.update_traces(marker_color='#CB7A5C')

    figSME = px.box(dfSME, x='Year',y=y,range_y=range_y,title='State-Influenced Market Economies',
                    labels = {'PubSpGDP': 'Public Spending as a % of GDP',
                              'PrivSpGDP': 'Private Spending as a % of GDP',
                              'IntRatioNonEU': 'Percentage International Students'})
    figSME.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 400,width=400)
    figSME.update_traces(marker_color='#5785C1')

    # Adding a trendline
    trendline_data = df.groupby('Year')[y].mean()
    figall.add_scatter(x=trendline_data.index, y=trendline_data.values, mode='lines',
                       name='Trendline', line=dict(color='black'))
    trendline_dataLME = dfLME.groupby('Year')[y].mean()
    figLME.add_scatter(x=trendline_dataLME.index, y=trendline_dataLME.values, mode='lines',
                       name='Trendline',line=dict(color='black'))
    trendline_dataCME = dfCME.groupby('Year')[y].mean()
    figCME.add_scatter(x=trendline_dataCME.index, y=trendline_dataCME.values, mode='lines',
                       name='Trendline',line=dict(color='black'))
    trendline_dataSME = dfSME.groupby('Year')[y].mean()
    figSME.add_scatter(x=trendline_dataSME.index, y=trendline_dataSME.values, mode='lines',
                       name='Trendline',line=dict(color='black'))

    #Disable zoom
    figall.layout.xaxis.fixedrange = True
    figall.layout.yaxis.fixedrange = True
    figLME.layout.xaxis.fixedrange = True
    figLME.layout.yaxis.fixedrange = True
    figCME.layout.xaxis.fixedrange = True
    figCME.layout.yaxis.fixedrange = True
    figSME.layout.xaxis.fixedrange = True
    figSME.layout.yaxis.fixedrange = True

    return figall, figLME, figCME, figSME