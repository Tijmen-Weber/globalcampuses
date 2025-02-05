import pandas as pd
import dash
from dash import callback, Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


#Defining the app
dash.register_page(__name__)

#create layout
layout = html.Div(style={'width':'810px','font-family':'sans-serif','fontSize': '14px'},children=[
    html.H1("Emigrerende en immigrerende internationale studenten"),
    html.Div([#first box containing the map
        dcc.RadioItems(#radioitems for incoming/outgoing/net migration
            id="worldmap of international students nl", #id for later
            options=[
                {'label':'Emigrerende internationale studenten','value':'Outgoing_Migration'},
                {'label':'Immigrerende internationale studenten','value':'Incoming_Migration'},
                {'label':'Migratiesaldo van internationale studenten','value':'Net_Migration'}],
            value='Outgoing_Migration',
            labelStyle={'display': 'block'},
            style={'display': 'flex', 'flex-direction': 'column','fontSize': '20px','font-family':'sans-serif'} #set display and direction
        ),
        dcc.Graph(id='worldmapnl',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
    ])
])
#create callback system
@callback(
    Output('worldmapnl','figure'),#id and type of output
    Input('worldmap of international students nl','value'))

#generate map
def generate_map(migration_type):
    df = pd.read_csv('Paper2_map_data_nl.csv',encoding = "ISO-8859-1") #load data
    df2018 = df.query('YEAR==2018') #select only 2018
    #datasets for outgoing
    dfout = df2018[df2018['Out_rel'] > 0]
    dfmisout = df2018.loc[df2018['Out_rel'].isna()] #missing data for net migration
    dfmisout['Out_rel'] = dfmisout['Out_rel'].fillna(0) #fill the missing data with 0s
    #dataset for incoming
    dfin = df2018[df2018['In_rel'] > 0]
    dfmisin = df2018.loc[df2018['In_rel'].isna()] #missing data for net migration
    dfmisin['In_rel'] = dfmisin['In_rel'].fillna(0) #fill the missing data with 0s
    #below three datasets are created for the three traces
    dfpos = df2018[df2018['INminOutrel'] > 0] #Positive net migration
    dfneg = df2018[df2018['INminOutrel'] <0] #Negative net migration
    dfmisnet = df2018.loc[df2018['INminOutrel'].isna()] #missing data for net migration
    dfmisnet['INminOutrel'] = dfmisnet['INminOutrel'].fillna(0) #fill the missing data with 0s

    figout = go.Choropleth(
        locations = dfout['NATc'],
        z = np.log(dfout['Out_rel']),
        locationmode = 'ISO-3',
        colorscale='Reds',
        text = list(dfout['NAT']),
        customdata=dfout['Out_rel'],
        hovertemplate="<b>%{text}</b><br>Emigratie: %{customdata:.2f}%",
        showscale = False,
        hoverlabel=dict(namelength=0))
    figmisout = go.Choropleth(
        locations = dfmisout['NATc'],
        z = dfmisout['Out_rel'],
        locationmode = 'ISO-3',
        colorscale=[(0,'white'),(1,'white')],
        text = list(dfmisout['NAT']),
        hovertemplate="<b>%{text}</b><br>Geen Data",
        showscale = False,
        hoverlabel=dict(namelength=0))
    figin = go.Choropleth(
        locations = dfin['NATc'],
        z = np.log(dfin['In_rel']),
        locationmode = 'ISO-3',
        colorscale='Blues',
        text = list(dfin['NAT']),
        customdata=dfin['In_rel'],
        hovertemplate="<b>%{text}</b><br>Immigratie: %{customdata:.2f}%",
        showscale = False,
        hoverlabel=dict(namelength=0))
    figmisin = go.Choropleth(
        locations = dfmisin['NATc'],
        z = dfmisin['In_rel'],
        locationmode = 'ISO-3',
        colorscale=[(0,'white'),(1,'white')],
        text = list(dfmisin['NAT']),
        hovertemplate="<b>%{text}</b><br>Geen Data",
        showscale = False,
        hoverlabel=dict(namelength=0))
    figpos = go.Choropleth( #positive trace
        locations = dfpos['NATc'],#locations are based on the ISO code in NATc
        z=np.log(dfpos['INminOutrel']), #z is the variable used for the colors. I log transform it to account for outliers (e.g. Australia)
        locationmode = 'ISO-3', #create z based on ISO
        colorscale='Blues', #blue for positive
        text = list(dfpos['NAT']), #create a list of country names (for the hovertemplate)
        customdata=dfpos['INminOutrel'], #for the hovertemplate
        hovertemplate="<b>%{text}</b><br>Net Migratie: %{customdata:.2f}%", #hovertext
        showscale = False, #remove the legend
        hoverlabel=dict(namelength=0)) #remove the trace part of the hovertext
    figneg = go.Choropleth(
        locations = dfneg['NATc'],
        z=np.log(np.absolute(dfneg['INminOutrel'])),
        locationmode = 'ISO-3',
        colorscale='Reds',
        text = list(dfneg['NAT']),
        customdata=dfneg['INminOutrel'],
        hovertemplate="<b>%{text}</b><br>Net Migratie: %{customdata:.2f}%",
        showscale = False,
        hoverlabel=dict(namelength=0))
    figmisnet = go.Choropleth(
        locations = dfmisnet['NATc'],
        z = dfmisnet['INminOutrel'],
        locationmode = 'ISO-3',
        colorscale=[(0,'white'),(1,'white')],
        text = list(dfmisnet['NAT']),
        hovertemplate="<b>%{text}</b><br>Geen Data",
        showscale = False,
        hoverlabel=dict(namelength=0))
    #linking migratin_type to the figures by storing them in the datat object which can then be used in the go.Figure
    if migration_type == 'Outgoing_Migration':
        datat = [figout,figmisout]
    elif migration_type == 'Incoming_Migration':
        datat = [figin,figmisin]
    else:
        datat = [figpos,figneg,figmisnet]

    fig = go.Figure(data=datat)
    fig.update_layout(
        autosize = True,
        height = 400,
        width = 810,
        margin=dict(l=0,t=0,b=0),
        title_font_family="sans-serif",
        dragmode=False)
    return fig




