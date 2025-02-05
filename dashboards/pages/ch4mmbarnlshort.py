import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv("ch4mmdata_nl.csv")
data = data[data['FOS'].isin(['Landbouw','Techniek','Taal en Cultuur'])]

dash.register_page(__name__)


#layout
layout = html.Div([
    html.H2("Populariteit van studierichtingen per ontwikkelingsniveau"),
    dcc.RadioItems(
        id='radioitems',
        options=[
            {'label':'Alle studies','value':'all'},
            {'label':'bachelor studies','value':'ba'},
            {'label':'master studies','value':'ma'}],
        value='all'),
    html.Div(dcc.Graph(id='mmbarnlshort',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}))],
    style={'font-family':'sans-serif'})

#callback
@callback(
    Output('mmbarnlshort','figure'),
    Input('radioitems','value'))

#graph
def update_mmbar(group):
    mask = data["group"] == group

    fig = px.bar(data[mask],
                        x="pred_rel",
                        y="FOS",
                        color="HDIq",
                        barmode='group',
                        orientation='h',
                        height=800,width=800,
                        color_discrete_map=({"1: Zeer laag":"#FBA72A",
                                             "2: Laag":"#D29E4f",
                                             "3: Midden":"#A99675",
                                             "4: Hoog":"#808D9b",
                                             "5: Zeer hoog":"#5785C1"}),
                        labels = {'FOS':'Studierichting',
                                  'pred_rel':'Percentage internationale studenten',
                                  'HDIq':'Ontwikkelingsniveau'},
                        #category_orders={'HDIq':['5: Zeer hoog','4: Hoog','3: Midden','2: Laag','1: Zeer laag']}
                        hover_data={'pred_rel': ':.1%'}
                        )
    fig.update_layout(
        yaxis={'categoryorder':'category descending'},
                             plot_bgcolor='white',
                             font_family="sans-serif",
        font_color="black",
        font_size=14)
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig

