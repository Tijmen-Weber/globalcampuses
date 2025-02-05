import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv("ch4mmdata.csv")

dash.register_page(__name__)


#layout
layout = html.Div([
    html.H2("Popularity of Field of Study per Level of Development"),
    dcc.RadioItems(
        id='radioitems',
        options=[
            {'label':'All Study Programs','value':'all'},
            {'label':'Bachelor Study Programs','value':'ba'},
            {'label':'Master Study Programs','value':'ma'}],
        value='all'),
    html.Div(dcc.Graph(id='mmbar',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}))],
    style={'font-family':'sans-serif'})

#callback
@callback(
    Output('mmbar','figure'),
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
                        color_discrete_map=({"1: Very Low":"#FBA72A",
                                             "2: Low":"#D29E4f",
                                             "3: Medium":"#A99675",
                                             "4: High":"#808D9b",
                                             "5: Very High":"#5785C1"}),
                        labels = {'FOS':'Field of Study',
                                  'pred_rel':'Percentage International Students',
                                  'HDIq':'Level of Development'},
                        #category_orders={'HDIq':['5: Very High','4: High','3: Medium','2: Low','1: Very Low']}
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

