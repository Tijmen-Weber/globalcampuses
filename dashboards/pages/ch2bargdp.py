import plotly.graph_objects as go
import dash
from dash import callback,html,dcc, Input, Output

#Defining the app
dash.register_page(__name__)

#Create variables
Quintile = ['Total','Very Low','Low','Medium','High','Very High'] #X data
Between_GDP = [222,110,189,263,376,400] #Y data 1
custom_labelsBR= ['222% more International Students',#label text 1
                  '110% more International Students',
                  '189% more International Students',
                  '263% more International Students',
                  '376% more International Students',
                  '400% more International Students'] 
Within_GDP = [42,21,52,34,45,40] #Y data 2
custom_labelsWR= ['42% more International Students',#label text 2
                  '21% more International Students',
                  '52% more International Students',
                  '34% more International Students',
                  '45% more International Students',
                  '40% more International Students'] 

#Create bars
bar1 = go.Bar(x=Quintile, y=Between_GDP, #X and Y
              marker=dict(color=['black','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue']),
              hovertemplate=custom_labelsBR, #hovertext becomes the custom_labels
              hoverlabel=dict(namelength=0)) #remove trace from hover text

bar2 = go.Bar(x=Quintile, y=Within_GDP, #X and Y
             marker=dict(color=['black','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue']),         
            hovertemplate=custom_labelsWR, #hovertext becomes the custom_labels
            hoverlabel=dict(namelength=0)) #remove trace from hover text

layout = html.Div([
    html.H1("Effect of Having a Higher GDP"),
    dcc.RadioItems(
        id='bar-selector',
        options=[
            {'label': 'GDP Between Countries', 'value': 'bar1'},
            {'label': 'GDP Within Countries', 'value': 'bar2'}
        ],
        value='bar1',  # Default to show bar1
        labelStyle={'display': 'inline-block', 'margin': '10px','fontFamily': 'serif', 'fontSize': '16px'}
    ),
    dcc.Graph(id='bar-graph-GDP')
])

# Define callback to switch between bars
@callback(Output('bar-graph-GDP', 'figure'), Input('bar-selector', 'value'))
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
                title='GDP Between Countries',
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
                title='GDP Within Countries',
                title_font=dict(size=24, family="serif"),
                autosize=False,
                width=700,
                height=500,
                showlegend=False
            )
        }
