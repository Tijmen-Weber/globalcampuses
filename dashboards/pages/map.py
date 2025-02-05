import pandas as pd
import plotly.express as px
import dash
from dash import callback, dcc, html, Input, Output




#Defining the app
dash.register_page(__name__)

#Creating layout
layout = html.Div([
    html.H1("International Students in the Netherlands"),
            html.Div([#first box containing the map
                dcc.Dropdown(#radioitems for absolute or relative international students
                    id="map of international students",
                    options=[
                        {'label':'Total Number of International Students','value':'International Students'},
                        {'label':'Percentage International Students (Muncipalities with at least 2000 students only)','value':'Percentage International Students1'},
                        {'label':'Percentage International Students (All Municipalities)','value':'Percentage International Students2'}],
                        value='International Students'),
                dcc.Graph(id='map')
                ],
                style={"width":"40%"},)
        ])

#Create callback system for map
@callback(
    Output('map','figure'),
    Input("map of international students",'value'))
#generate map
def generate_map(dataset):
    dfmapabs = pd.read_csv('map_data.csv') #read data
    #creating relative data1
    dfmaprel1 = pd.read_csv('map_data.csv')
    munaverages = dfmaprel1.groupby('MUN')['TOT_STUD'].transform('mean') #create datafile with Mun averages
    dfmaprel1['MUNavg'] = munaverages
    dfmaprel1.loc[dfmaprel1['MUNavg'] > 1999,'REL_STUD'] = round(dfmaprel1['REL_STUD']*100,1) #create % international students
    dfmaprel1.loc[dfmaprel1['MUNavg'] < 2000,'REL_STUD'] = None #if total students is <2000
    dfmaprel1 = dfmaprel1.dropna() #remove missing values from data
    dfmaprel1 = dfmaprel1.drop(columns="INT_STUD") #drop absolute

    #creating relative data2
    dfmaprel2 = pd.read_csv('map_data.csv')
    dfmaprel2['REL_STUD'] = round(dfmaprel2['REL_STUD']*100,1)

    dfmapabs = dfmapabs.rename(columns = {"INT_STUD":"International Students"})
    dfmaprel1 = dfmaprel1.rename(columns = {"REL_STUD":"International Students"}) #rename the % international students column
    dfmaprel2 = dfmaprel2.rename(columns = {"REL_STUD":"International Students"})
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
                         size="International Students", #make the size of the bubbles scale with international students
                         animation_frame="YEAR", #Animation (size changes over the years)
                         width=750, #width of the figure
                         height=800, #height of the figure
                         zoom=5, #how much it is zoomed out
                         size_max=100,#size of the bubbles
                         title="Map of International Students per Municipality")
    fig.update_layout(mapbox_bounds={"west": 3, "east": 7.5, "south": 50.5, "north": 53.8}) #boundaries of the map
    fig.update_layout(
        mapbox_style="open-street-map",#map style
        title_font_family="Open Sans",
        title_font_color="black",
        title_font_size=22,
        font_family="Open Sans",
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
    return fig

