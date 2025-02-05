
#Packages
import pandas as pd
import plotly.express as px
from dash import callback, Dash, dcc, html, Input, Output
import dash


df = pd.read_excel('Total Data nov 2021.xlsx')


#Defining the app
dash.register_page(__name__)

layout = html.Div([
    html.H2("Spending on Higher Education per Country"),#title
    dcc.RadioItems(#radioitems
        id='radioitems',
        options=[
            {'label':'Public Spending on Higher Education','value':'PubSpGDP'},#label is the name in the dropdown, value is the name of the column in the data
            {'label':'Private Spending on Higher Education','value':'PrivSpGDP'}],
        value='PubSpGDP'),
    html.Div(dcc.Graph(id='line',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}))],
    style={'font-family':'sans-serif'})

@callback(
    Output("line", "figure"),
    Input("radioitems", "value")
    )

def update_line_chart(y):
    fig = px.line(df,
                  x='Year',
                  y=y,
                  color='Country',
                  line_group = 'Country',
                  labels = {'PubSpGDP': 'Public Spending as a % of GDP',
                            'PrivSpGDP': 'Private Spending as a % of GDP'})
    fig.update_layout(plot_bgcolor='white',yaxis=dict(hoverformat='.1f'),
                         height = 600,width=800,font_family='sans-serif')
    fig.layout.xaxis.fixedrange = True #Disable zoom
    fig.layout.yaxis.fixedrange = True

    return fig
