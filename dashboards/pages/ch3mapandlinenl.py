
import pandas as pd
import plotly.express as px
import dash
from dash import callback, Dash, dcc, html, Input, Output


#Defining the app
dash.register_page(__name__)

#Creating layout
layout = html.Div([
    html.H1("Internationale studenten in Nederland"),
        html.Div([#second box
            html.Div([#first box containing the map
                html.H2("Kaart van internationale studenten per gemeente"),
                dcc.Dropdown(#radioitems for absolute or relative international students
                    id="map of international students",
                    options=[
                        {'label':'Totaal aantal internationale studenten','value':'International Students'},
                        {'label':'Percentage internationale studenten (alleen gemeentes met tenminste 2000 studenten)','value':'Percentage International Students1'},
                        {'label':'Percentage internationale studenten (alle gemeentes)','value':'Percentage International Students2'}],
                        value='International Students'),
                dcc.Graph(id='ch3map',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
                ],
                style={'padding':1,'flex':1}),
            html.Div([#second box containing the line chart
                html.H2('Groei in het aantal eerstejaars internationale studenten'),
                dcc.Dropdown( #dropdown
                    id="abs_rel",
                    options=[
                        {'label':'Totaal aantal internationale studenten', 'value':'Internationale Studenten'},
                        {'label':'Percentage internationale studenten','value':'Percentage Internationale Studenten'}],
                        value='Internationale Studenten'),
                dcc.Graph(id='ch3linechartnl',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}),#graph first here
                dcc.Checklist( #checklist 1
                    id="municipalities",
                    options= sorted(pd.read_csv('ch3map_data.csv').MUN.unique()),#this creates an alphabetical list of unique municipality names
                    inline=False, #this arranges them horizontally
                    value=['Arnhem','Nijmegen'], #set Arnhem and Nijmegen as default
                    className = 'checklist-grid')

                ],
                style={'display':'flex','flex-direction':'column','font-family':'sans-serif'}
                    )
                ],
                 style={'display':'flex',
                        'flex-direction':'column', #make them below each other
                        'width' : '800px',#Change width to 800 pixels
                        'font-family':'sans-serif'})
],style={'font-family':'sans-serif'})

#Create callback system for map
@callback(
    Output('ch3mapnl','figure'),
    Input("map of international students",'value'))
#generate map
def generate_map(dataset):
    dfmapabs = pd.read_csv('ch3map_data.csv') #read data and use this for the absolute dataset

    #creating relative data1
    dfmaprel1 = pd.read_csv('ch3map_data.csv')
    munaverages = dfmaprel1.groupby('MUN')['TOT_STUD'].transform('mean') #create datafile with Mun averages
    dfmaprel1['MUNavg'] = munaverages
    dfmaprel1.loc[dfmaprel1['MUNavg'] > 1999,'REL_STUD'] = round(dfmaprel1['REL_STUD']*100,1) #create % international students
    dfmaprel1.loc[dfmaprel1['MUNavg'] < 2000,'REL_STUD'] = None #if total students is <2000
    dfmaprel1 = dfmaprel1.dropna() #remove missing values from data
    dfmaprel1 = dfmaprel1.drop(columns="INT_STUD") #drop absolute

    #creating relative data2
    dfmaprel2 = pd.read_csv('ch3map_data.csv')
    dfmaprel2['REL_STUD'] = round(dfmaprel2['REL_STUD']*100,1)

    dfmapabs = dfmapabs.rename(columns = {"INT_STUD":"Internationale Studenten"})
    dfmaprel1 = dfmaprel1.rename(columns = {"REL_STUD":"Internationale Studenten"}) #rename the % international students column
    dfmaprel2 = dfmaprel2.rename(columns = {"REL_STUD":"Internationale Studenten"})
    if dataset == "International Students":
        data = dfmapabs
    elif dataset == 'Percentage International Students1':
        data = dfmaprel1
    else:
        data=dfmaprel2
    fig = px.scatter_mapbox(data,  #data
                         lat="lat", #latitude
                         lon="lng", #longitude
                         hover_name="MUN", #title of hover text
                         hover_data={'YEAR':False,#removes YEAR, lat, and long from the hover text
                                     'lat':False,
                                     'lng':False},
                         size="Internationale Studenten", #make the size of the bubbles scale with international students
                         animation_frame="YEAR", #Animation (size changes over the years)
                         width=750, #width of the figure
                         height=800, #height of the figure
                         zoom=5, #how much it is zoomed out
                         size_max=100,#size of the bubbles
                         title="Kaart van het aantal internationale studenten per gemeente")
    fig.update_layout(mapbox_bounds={"west": 3, "east": 7.5, "south": 50.5, "north": 53.8}) #boundaries of the map
    fig.update_layout(
        mapbox_style="open-street-map",#map style
        title_font_family="sans-serif",
        title_font_color="black",
        title_font_size=22,
        font_family="sans-serif",
        font_color="black",
        font_size=14)
    fig.update_layout(updatemenus=[dict(type='buttons',  # position the buttons (closer to the plot) (from: https://community.plotly.com/t/how-can-i-move-the-animation-play-button-and-slider-closer-to-the-plot/48646)
                  showactive=False,
                  y=-0.10,
                  x=-0.05,
                  xanchor='left',
                  yanchor='bottom')
                        ])
    fig['layout']['sliders'][0]['pad']=dict(r= 70, t= 0.0,)# position the slider (closer to the plot)
    fig.layout.xaxis.fixedrange = True #disable zoom
    fig.layout.yaxis.fixedrange = True
    return fig

#Create callback system for linechart
@callback(
    Output('ch3linechartnl','figure'),
    [Input('municipalities','value'),
     Input('abs_rel','value')])

#generate line chart
def generate_linechart(Mun,abs_rel):
    dfline = pd.read_csv('ch3map_data.csv')
    mask = dfline.MUN.isin(Mun) #isin filters. So a filter is created based on the input
    dfline = dfline.rename(columns={'INT_STUD':'Internationale Studenten','REL_STUD':'Percentage Internationale Studenten'})  # Rename the selected column
    dfline['Percentage Internationale Studenten'] = round(dfline['Percentage Internationale Studenten']*100,1)
    fig = px.line(dfline[mask], #the dataset is filtered each time here
        x='YEAR',
        y=abs_rel,
        color='MUN', #lines split up by municipality
        labels={'YEAR':'Jaar',
                "MUN":'Gemeente'},#note that label is not just for axes but also for legend
        template='simple_white') #white background template
    fig.update_yaxes(showgrid=True) #Show horizontal grid
    fig.update_layout( #change font etc.
        title_font_family="sans-serif",
        title_font_color="black",
        title_font_size=22,
        font_family="sans-serif",
        font_color="black",
        font_size=14)
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    return fig








