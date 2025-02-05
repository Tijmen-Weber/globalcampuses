import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv('CH3_linechart2_data.csv')

dash.register_page(__name__)

#Creating layout
layout = html.Div([
    html.H1("International Students per Study Type"),
    html.Div([
        dcc.RadioItems(
            id='abs_rel',
            options = [
                {'label':'Absolute Number of International Students','value':'INT_STUD'},
                {'label':'Relative Number of International Students','value':'INT_SHARE'}],
                value = 'INT_STUD'),
            dcc.Graph(id='ch3_linechart2',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']})]
            )],
    style={'width':'800px', 'font-family':'sans-serif'})

@callback(
    Output('ch3_linechart2','figure'),
    Input("abs_rel",'value'))

def generate_linechart(abs_rel):
    fig = px.line(data,
                  x='YEAR',
                  y=abs_rel,
                  color='Type',
                  color_discrete_sequence=["#FBA72A", "#a9a9a9", "#CB7A5C", "#5785C1"],
                  labels={'YEAR':'Year',
                          'INT_STUD':'Number of International Students',
                          'INT_SHARE':'Percentage International Students'},#note that label is not just for axes but also for legend
                  template='simple_white')
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        legend_title = 'Type of Study Program',
        yaxis = dict(hoverformat='.0f'))
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    return fig

