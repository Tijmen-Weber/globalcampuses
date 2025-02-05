import pandas as pd
import plotly.express as px
import dash
from dash import callback, dcc, html, Input, Output

dfmap = pd.read_csv('map_data.csv') #read data

#Defining the app
dash.register_page(__name__)

#Creating layout
layout = html.Div([
    html.H1("Growth in International Students per Municipality"),
    html.Div([#second box containing the line chart
                dcc.Graph(id='linechart'),#graph first here
                dcc.Checklist( #checklist with the municipalities
                    id="municipalities",
                    options= sorted(dfmap.MUN.unique()),#this creates an alphabetical list of unique municipality names
                    inline=True, #this arranges them horizontally
                    value=['Arnhem','Nijmegen']) #set Arnhem and Nijmegen as default
                ],
                style={'padding':10,'flex':1})
    ])

#Create callback system for linechart
@callback(
    Output('linechart','figure'),
    Input('municipalities','value'))
#generate line chart
def generate_linechart(Mun):
    dfmap = pd.read_csv('map_data.csv') #read data
    dfmap['REL_STUD'] = round(dfmap['REL_STUD']*100,1)#transform the REL_STUD variable into percentage with 1 decimal
    dfmap = dfmap.rename(columns = {"INT_STUD":"International Students",#rename the international student column
                              "REL_STUD":"Percentage International Students"}) #rename the % international students column
    mask = dfmap.MUN.isin(Mun) #isin filters. So a filter is created based on the input
    fig = px.line(dfmap[mask], #the dataset is filtered each time here
        x='YEAR',
        y='International Students',
        color='MUN', #lines split up by municipality
        title='Growth in International Students per Municipality',
        labels={'YEAR':'Year',
                "MUN":'Municipality'},#note that label is not just for axes but also for legend
        template='simple_white') #white background template
    fig.update_yaxes(showgrid=True) #Show horizontal grid
    fig.update_layout( #change font etc. 
        title_font_family="Open Sans",
        title_font_color="black",
        title_font_size=22,
        font_family="Open Sans",
        font_color="black",
        font_size=14)
    return fig



                  