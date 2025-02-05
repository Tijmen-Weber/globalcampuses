import plotly.graph_objects as go
import dash
from dash import html,dcc, Input, Output, callback

#Defining the app
dash.register_page(__name__)

#Create variables
Quintile = ['Total','Very Low','Low','Medium','High','Very High'] #X data
Between_Ranking = [-2,-9,4,-10,-1,7] #Y data 1
custom_labelsBR= ['No Significant Change',
                  '9% less International Students',
                  '4% more International Students',
                  '10% less International Students',
                  'No Significant Change',
                  '7% more International Students'] #label text 1
Within_Ranking = [2,7,4,0.2,2,-2] #Y data 2
custom_labelsWR= ['2% more International Students',
                  '7% more International Students',
                  '4% more International Students',
                  'No Significant Change',
                  'No Significant Change',
                  'No Significant Change'] #label text 2

#Create bars
bar1 = go.Bar(x=Quintile, y=Between_Ranking, #X and Y
            marker={'color':['black','indianred','RoyalBlue','indianred','indianred','RoyalBlue'], #set color of bars
                   'opacity':[0.15,1,1,1,0.15,1]}, #set opacity of bars                   
            hovertemplate=custom_labelsBR, #hovertext becomes the custom_labels
            hoverlabel=dict(namelength=0)) #remove trace from hover text
#potential colors: indianred, 
bar2 = go.Bar(x=Quintile, y=Within_Ranking, #X and Y
            marker={'color':['black','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue','indianred'], #set color of bars
                   'opacity':[1,1,1,0.15,0.15,0.15]}, #set opacity of bars          
            hovertemplate=custom_labelsWR, #hovertext becomes the custom_labels
            hoverlabel=dict(namelength=0)) #remove trace from hover text


layout = html.Div([
    html.H1("Effect of Having a Higher Ranking"),
    dcc.RadioItems(
        id='bar-selector',
        options=[
            {'label': 'Ranking Between Countries', 'value': 'bar1'},
            {'label': 'Ranking Within Countries', 'value': 'bar2'}
        ],
        value='bar1',  # Default to show bar1
        labelStyle={'display': 'inline-block', 'margin': '10px','fontFamily': 'serif', 'fontSize': '16px'}
    ),
    dcc.Graph(id='bar-graph-ranking')
])

# Define callback to switch between bars
@callback(Output('bar-graph-ranking', 'figure'), Input('bar-selector', 'value'))
def update_graph(bar):
    if bar == 'bar1':
        return {
            'data': [bar1],
            'layout': go.Layout(
                xaxis=dict(
                    title='Development Level of Origin Countries',
                    title_font=dict(family="serif", size=20)
                ),
                yaxis=dict(
                    title='% Increase in International Students',
                    title_font=dict(family="serif", size=20)
                ),
                title='Ranking Between Countries',
                title_font=dict(size=24, family="serif"),
                autosize=False,
                width=700,
                height=500,
                showlegend=False,
            )
        }
    elif bar == 'bar2':
        return {
            'data': [bar2],
            'layout': go.Layout(
                xaxis=dict(
                    title='Development Level of Origin Countries',
                    title_font=dict(family="serif", size=20)
                ),
                yaxis=dict(
                    title='% Increase in International Students',
                    title_font=dict(family="serif", size=20)
                ),
                title='Ranking Within Countries',
                title_font=dict(size=24, family="serif"),
                autosize=False,
                width=700,
                height=500,
                showlegend=False
            )
        }


