import plotly.graph_objects as go
import dash
from dash import html,dcc, Input, Output, callback

#Defining the app
dash.register_page(__name__)

#Create variables
Quintile = ['Total','Very Low','Low','Medium','High','Very High'] #X data
Common_Language = [938,1070,1094,750,357,80] #Y data 1
custom_labelsCL= ['938% more International Students',#label text 1
                  '1070% more International Students',
                  '1094% more International Students',
                  '750% more International Students',
                  '357% more International Students',
                  '80% more International Students'] 
Colonial_Past = [346,362,310,464,267,146] #Y data 2
custom_labelsCP= ['346% more International Students',#label text 2
                  '362% more International Students',
                  '310% more International Students',
                  '464% more International Students',
                  '267% more International Students',
                  '146% more International Students'] 

#Create bars
bar1 = go.Bar(x=Quintile, y=Common_Language, #X and Y
              marker=dict(color=['black','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue']),
            hovertemplate=custom_labelsCL, #hovertext becomes the custom_labels
            hoverlabel=dict(namelength=0)) #remove trace from hover text

bar2 = go.Bar(x=Quintile, y=Colonial_Past, #X and Y
             marker=dict(color=['black','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue','RoyalBlue']),         
            hovertemplate=custom_labelsCP, #hovertext becomes the custom_labels
            hoverlabel=dict(namelength=0)) #remove trace from hover text


layout = html.Div([
    html.H1("Effect of Having a Common Language and a Colonial History"),
    dcc.RadioItems(
        id='bar-selector',
        options=[
            {'label': 'Sharing a Common Language', 'value': 'bar1'},
            {'label': 'Having a Colonial History', 'value': 'bar2'}
        ],
        value='bar1',  # Default to show bar1
        labelStyle={'display': 'inline-block', 'margin': '10px','fontFamily': 'serif', 'fontSize': '16px'}
    ),
    dcc.Graph(id='bar-graph-langcol')
])

# Define callback to switch between bars
@callback(Output('bar-graph-langcol', 'figure'), Input('bar-selector', 'value'))
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
                title='Sharing a Common Language',
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
                title='Having a Colonial History',
                title_font=dict(size=24, family="serif"),
                autosize=False,
                width=700,
                height=500,
                showlegend=False
            )
        }

