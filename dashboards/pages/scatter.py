import plotly.graph_objects as go
import pandas as pd
import dash
from dash import  dcc, html




df = pd.read_csv('Scatter_Loess_data.csv')
df['Migration_rel'] = df['Migration_rel']/10
df['pred_y'] = df['pred_y']/10

# make figure
fig_dict = {#dictionary containing the framework of the figure. Right now empty to be filled in later.
    "data": [],
    "layout": {},
    "frames": []
}

#Make layout
fig_dict["layout"]["title"] = {'text':"Development and International Students",
                               'font':{'size':28,'family':'sans-serif','color':'black'}}
fig_dict["layout"]["xaxis"] = {"range": [0.25,1], #sets the limits of the axes
                               "title": "Human Development Index",#Axis title
                               'titlefont':{'size':20,'family':'sans-serif','color':'black'},
                               'showline':True, #adds a line on the axe
                               'linecolor':'black', #makes the line black
                               'mirror':True} #puts the line on the other side
fig_dict["layout"]["yaxis"] = {"range":[0,8.5], #range. Note that Australia now falls outside of it
                               'title':'International Students as a % of the Population Aged 15-24',
                               'titlefont':{'size':16,'family':'sans-serif','color':'black'},
                               'showline':True,'linecolor':'black','mirror':True} #creating border
fig_dict["layout"]["legend"] = {"font":{"size":16,"family":"sans-serif",'color':'black'}}
fig_dict["layout"]['width'] = 850
fig_dict["layout"]['height'] = 750
fig_dict["layout"]['autosize'] = False
fig_dict["layout"]['plot_bgcolor'] = "white"
fig_dict["layout"]["updatemenus"] = [ {
    "buttons":[{
        'args': [None,{"frame": {"duration": 500, "redraw": False}, #the frame is another dict containing two things. duration means it linger for 500ms on each frame. redraw: False means it isn't redrawn after each frame (but setting it to True doesn't change anything?)
                        "fromcurrent": True, #Fromcurrent True means it continues from where it's at when paused. If set to False it will start from the beginning.
                        "transition": {"duration": 0,#transition duration means how long the transition between the frames last.
                                       "easing": "linear"}}],#easing is the kind of animation. More options available here: https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
        "label": "Play", #This is just the text on the button
        "method": "animate" #method refers to what it should trigger, in this case an animation
    },
        {
            "args": [[None], #By changing it to [None] instead of None it is changed from a pause to a play button. This is because the list [None] is passed as an argument to the method=animate and therefore tells it not to animate, i.e. to pause.
                     {"frame": {"duration": 0, "redraw": False}, #I think this is just superfluous.
                              "mode": "immediate", #this just means that the animation is played without delay or animation
                              "transition": {"duration": 0}}], #probably also superfluous.
            "label": "Pause",
            "method": "animate"
        }
    ],
    "direction": "left", #direction of how the buttons are laid out. E.g. changing it to up has play placed above pause
    "pad": {"r": 12, "t": 87}, #sets padding around the button. r is padding on right side. t is padding on top
    "showactive": False, #If set to true is supposed to highlight the button but it doesn't do anything?
    "type": "buttons", #can be changed to dropdown to create an additional clickable dropdown menu
    "x": 0.1, #now set to 0.1 if changed to a higher will move the button to the right
    "xanchor": "right", #binds it to the left, right, or center of the range selector (but changing it to center or left actually makes it move closer to the slider)
    "y": 0, #y coordinate. if set to 3 will be much higher.
    "yanchor": "top", #binds it to the top. Changing it to middle or bottom makes the button appear higher though.
    "font":{"family":"sans-serif","size":16,'color':'black'}
        }]



#make data
#First frame (serving as data argument in the go.Figure)
dfg = df[df["YEAR"]==2003] #The first frame is 2003, hence this selection
dfgo = dfg[dfg["Type"]=="Outbound"] #selecting only outbound migration
dfgi = dfg[dfg["Type"]=="Inbound"] #selecing only inbound migration
#Scatter outbound
data_dict_scatter_out = {
    "x": list(dfgo['HDI']),
    "y": list(dfgo['Migration_rel']),
    "mode": "markers", #this creates the dots
    'marker': {
        'color':'#316395',#change the color (it seems it also changes this for all the frames)
        'symbol':'circle'}, #see: https://plotly.com/python/marker-style/
    "name": "Outgoing", #the name that appears in the legend and hovertext
    'text': list(dfgo['NAT']), #text that appears in the hovertext
    'hovertemplate':"<b>%{text}</b><br>" +
                    "International Students: %{y:.0f}%<br>" +
                    "Human Development Index: %{x:.3f}"
    }
#Scatter inbound
data_dict_scatter_in = {
    "x": list(dfgi['HDI']),
    "y": list(dfgi['Migration_rel']),
    "mode": "markers",
    'marker': {
        'color':'#FF9900'},
    "name": "Incoming",
    'text':list(dfgi['NAT']),
    'hovertemplate':"<b>%{text}</b><br>" +
                    "International Students: %{y:.0f}%<br>" +
                    "Human Development Index: %{x:.3f}"
    }
#Line outbound
data_dict_line_out = {
    "x": list(dfgo['new_x']),
    "y": list(dfgo['pred_y']),
    "mode": "lines",
    'line':{
        'color':'#316395'},
    "name": "Average Outgoing",
    'hovertemplate':"<b>Loess Line</b><br>"
                        "International Students: %{y:.0f}%<br>"
                        "Human Development Index: %{x:.3f}"
    }
#line inbound
data_dict_line_in = {
    "x": list(dfgi['new_x']),
    "y": list(dfgi['pred_y']),
    "mode": "lines",
    'line':{
        'color':'#FF9900'},
    "name": "Average Incoming",
    'hovertemplate':"<b>Loess Line</b><br>"
                        "International Students: %{y:.0f}%<br>"
                        "Human Development Index: %{x:.3f}"
    }
#append to the fig_dict
fig_dict['data'].append(data_dict_scatter_out)
fig_dict['data'].append(data_dict_scatter_in)
fig_dict['data'].append(data_dict_line_out)
fig_dict['data'].append(data_dict_line_in)

#Generate the slider
slider_dict = {
    "active":0,#make the slider start at the beginning
    "transition": {"duration": 0, "easing": "linear"}, #transition of the slider animation, duration and type of animation. Duration now set to 0 to avoid the wonky animations
    "pad": {"b": 10, "t": 55}, #padding around the slder
    "len": 0.9, #length of the slider
    "x": 0.1, #x coordinate of the slider
    "y": 0, #y coordinate of the slider
    "currentvalue": { #dict for a label for the slider
        "font": {"family":"sans-serif","size": 15}, #sets the size of the font
        "prefix": "Year:", #prefix of the label
        "visible": True, #if set to false, removes the label
        "xanchor": "right"}, #sets alignment relative to the slider
    "steps": [] #determining the steps of the slider. Now an empty list, to be filled in later
}

#Make frames
years = (df['YEAR'].unique()) #create list containing the values of the years

for year in years:
    frame = {"data": [], "name": str(year)}
    dfg = df[df["YEAR"]==year]
    dfgo = dfg[dfg["Type"]=="Outbound"]
    dfgi = dfg[dfg["Type"]=="Inbound"]
    #Scatter outbound
    data_dict_scatter_out = {
        "x": list(dfgo['HDI']),
        "y": list(dfgo['Migration_rel']),
        "mode": "markers",
        "name": "Outgoing",
        'text': list(dfgo['NAT'])
        }
    frame["data"].append(data_dict_scatter_out)
    #Scatter inbound
    data_dict_scatter_in = {
        "x": list(dfgi['HDI']),
        "y": list(dfgi['Migration_rel']),
        "mode": "markers",
        "name": "Incoming",
        'text': list(dfgi['NAT'])
        }
    frame["data"].append(data_dict_scatter_in)
    #Line outbound
    data_dict_line_out = {
        "x": list(dfgo['new_x']),
        "y": list(dfgo['pred_y']),
        "mode": "lines",
        "name": "Average Outgoing"
        }
    frame["data"].append(data_dict_line_out)
    #line inbound
    data_dict_line_in = {
        "x": list(dfgi['new_x']),
        "y": list(dfgi['pred_y']),
        "mode": "lines",
        "name": "Average Incoming"
        }
    frame["data"].append(data_dict_line_in)
    fig_dict['frames'].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False}, #durcation animation etc.
         "mode": "immediate",
         "transition": {"duration": 0}}
    ],
        "label": str(year), #label
        "method": "animate"} #and animate it
    slider_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [slider_dict]



fig = go.Figure(fig_dict)

fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True

#Defining the app
dash.register_page(__name__)

layout = html.Div(
    dcc.Graph(figure=fig,config={'modeBarButtonsToRemove': ['lasso2d', 'select2d']}))











