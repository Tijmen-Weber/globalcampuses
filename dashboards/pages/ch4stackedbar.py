import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv("ch4fig1data.csv")

dash.register_page(__name__)

#graph
stackedbar = px.bar(data,
                    x="STUD",
                    y="FOS",
                    color="Type",
                    orientation='h',
                    height=400,width=800,
                    color_discrete_map=({"Research University Master":"#D7A04E",
                                         "Research University Bachelor":"#B8836F",
                                         "University of Applied Science":"#6987AF"}),
                    labels = {'FOS':'Field of Study','STUD':'International Students'}
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
    html.H2("Total Number of Enrollments of First-Year International Students, 2016-2019"),
    html.Div(dcc.Graph(id='stackedbar',
        figure=stackedbar,config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
        ))],
    style={'font-family': 'sans-serif'})
