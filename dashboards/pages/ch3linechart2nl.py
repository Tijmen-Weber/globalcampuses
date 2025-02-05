import pandas as pd
import plotly.express as px
from dash import callback, dcc, html, Input, Output
import dash

data = pd.read_csv('CH3_linechart2_data_nl.csv')

dash.register_page(__name__)

#Creating layout
layout = html.Div([
    html.H1("Internationale studenten per type opleiding"),
    html.Div([
        dcc.RadioItems(
            id='abs_rel',
            options = [
                {'label':'Absolute aantal internationale studenten','value':'INT_STUD'},
                {'label':'Relatieve aantal internationale studenten','value':'INT_SHARE'}],
                value = 'INT_STUD'),
            dcc.Graph(id='ch3_linechart2nl',config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']})]
            )],
    style={'width':'800px', 'font-family':'sans-serif'})

@callback(
    Output('ch3_linechart2nl','figure'),
    Input("abs_rel",'value'))

def generate_linechart(abs_rel):
    fig = px.line(data,
                  x='YEAR',
                  y=abs_rel,
                  color='Type',
                  color_discrete_sequence=["#FBA72A", "#a9a9a9", "#CB7A5C", "#5785C1"],
                  labels={'YEAR':'Jaar',
                          'INT_STUD':'Aantal internationale studenten',
                          'INT_SHARE':'Percentage internationale studenten'},#note that label is not just for axes but also for legend
                  template='simple_white')
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        legend_title = 'Type opleiding',
        yaxis = dict(hoverformat='.0f'))
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    return fig

