
#Packages
import pandas as pd
import plotly.express as px
from dash import callback, Dash, dcc, html, Input, Output
import dash


df = pd.read_csv('Total_Data_nov_2021_nl.csv',encoding='utf-8')

#Defining the app
dash.register_page(__name__)

layout = html.Div([
    html.H2("Financiering van het hoger onderwijs per land"),#title
    dcc.RadioItems(#radioitems
        id='radioitems',
        options=[
            {'label':'Overheidsuitgaven aan het hoger onderwijs','value':'PubSpGDP'},#label is the name in the dropdown, value is the name of the column in the data
            {'label':'Particuliere uitgaven aan het hoger onderwijs','value':'PrivSpGDP'}],
        value='PubSpGDP'),
    html.Div(dcc.Graph(id='linech5nl',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}))],
    style={'font-family':'sans-serif'})

@callback(
    Output("linech5nl", "figure"),
    Input("radioitems", "value")
    )

def update_line_chart(y):
    fig = px.line(df,
                  x='Year',
                  y=y,
                  color='Country',
                  line_group = 'Country',
                  labels = {'PubSpGDP': 'Overheidsuitgaven als % van het BBP',
                            'PrivSpGDP': 'Particuliere uitgaven als % van het BBP',
                            'Country':'Land',
                            'Year':'Jaar'
})
    fig.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 600,width=800,font_family='sans-serif')
    fig.layout.xaxis.fixedrange = True #Disable zoom
    fig.layout.yaxis.fixedrange = True

    return fig