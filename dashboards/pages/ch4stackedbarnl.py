import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv("ch4fig1data_nl.csv")

dash.register_page(__name__)

#graph
stackedbar = px.bar(data,
                    x="STUD",
                    y="FOS",
                    color="Type",
                    orientation='h',
                    height=400,width=800,
                    color_discrete_map=({"Universiteit master":"#D7A04E",
                                         "Universiteit bachelor":"#B8836F",
                                         "Hogeschool":"#6987AF"}),
                    labels = {'FOS':'Studierichting','STUD':'Internationale studenten'}
                    )
stackedbar.update_layout(yaxis={'categoryorder':'total ascending'},
                         plot_bgcolor='white',
                         font_family="sans-serif",
                        font_color="black",
                        font_size=14)
stackedbar.layout.xaxis.fixedrange = True
stackedbar.layout.yaxis.fixedrange = True

#layout
layout = html.Div([
    html.H2("Totaal aantal inschrijven van eerstejaars internationale studenten 2016-2019"),
    html.Div(dcc.Graph(id='stackedbar',
        figure=stackedbar,config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
        ))],
    style={'font-family': 'sans-serif'})
