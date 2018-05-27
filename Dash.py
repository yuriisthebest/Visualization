# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import flask
import os

# My packages
from Storage import Data
dataset = Data()


# Constants
imageroute = '/MetroMapsEyeTracking/stimuli/'
defaultmap = '03_Bordeaux_S1.jpg'

def figure_layout(new_mapname):
    """
    Creates a graph with the image of the input puzzle under it

    :author: Yuri Maas
    :param input_value: The name of the puzzle to be in the graph
    """
    if new_mapname == None:
        return {}

    return {
        'data': [
            {
                'x': [0, dataset.get_resolution_X(new_mapname)],
                'y': [0, dataset.get_resolution_Y(new_mapname)],
            }
        ],
        'layout': go.Layout(
            images=[
                dict(
                    source=imageroute + new_mapname,
                    xref='x',
                    yref='y',
                    x=0,
                    y=0,
                    sizex= dataset.get_resolution_X(new_mapname),
                    sizey= dataset.get_resolution_Y(new_mapname),
                    xanchor='left',
                    yanchor='bottom',
                    #opacity=0.8,
                    layer='below'
                )
            ],
            title='Graph',
            xaxis = dict(
                range= [0, dataset.get_resolution_X(new_mapname)]
            ),
            yaxis = dict(
                range= [0, dataset.get_resolution_Y(new_mapname)]
            ),
            #height= dataset.get_resolution_Y(new_mapname),
            #width= dataset.get_resolution_X(new_mapname) - 300
        )
    }



app = dash.Dash()

app.layout = html.Div([
    # Global Structure ->   Input,
    #                           - Open & Save
    #                           - Panels
    #                           - Visualization Options
    #                           - Options for the visualizations
    #                       Visualization,
    #                           Plots
    #                       Output
    html.Div(
        id='Input-column',
        style={
            'width': '12%',
            'display': 'inline-block',
            'marginLeft' : 5,
            'marginRight': 5
        },
        children=[
            html.H1('Input'),

            html.Div(
                id= 'Input-head',
                children=[
                    html.H3('Open & Save'),
                    dcc.Upload(
                        id='Input-head-upload',
                        multiple= False,
                        style= {
                            'width': '100%',
                            'heigth': '60px',
                            'margin': '10px'
                        },
                        children= html.Div(
                            html.Button('Upload File')
                        )
                    ),

                    # What are we saving here?????
                    dcc.Upload(
                        id='Input-head-save',
                        multiple= False,
                        style= {
                            'width': '100%',
                            'heigth': '60px',
                            'margin': '10px'
                        },
                        children=[
                            html.Button('Save as')
                        ]
                    ),
                    html.Hr()
                ]
            ),

            html.Div(
                id= 'Input-panels',
                children=[
                    dcc.RadioItems(
                        options=[
                            {'label': 'Panel 1 (Top-Left)', 'value': 0},
                            {'label': 'Panel 2 (Top-Right)', 'value': 1},
                            {'label': 'Panel 3 (Bottom-Left)', 'value': 2},
                            {'label': 'Panel 4 (Bottom-Right)', 'value': 3}
                        ],
                        labelStyle= {'display': 'inline-block'}
                    ),
                    html.Hr()
                ]
            ),

            html.Div(
                id= 'Input-vis_options',
                children=[
                    dcc.RadioItems(
                        options=[
                            {'label': 'Adjacency Matrix', 'value': 0},
                            {'label': 'Metro Map', 'value': 1}
                        ],
                        labelStyle= {'display': 'inline-block'}
                    )
                ]
            ),

            html.Div(
                id= 'Input-add_options'
            ),

            html.Div(
                id= 'THE REST, WIP',
                children=[
                    html.Label('Puzzle:'),
                    dcc.Dropdown(
                        id= 'puzzle-dropdown',
                        value= defaultmap,
                        options = dataset.get_puzzlenames()
                    )
                ]
            ),
        ]
    ),


    html.Div(
        id='Visualization',
        style={
            'width': '65%',
            'display': 'inline-block',
            'marginLeft': 5,
            'marginRight': 5
        },
        children=[
            html.H1('Plots'),

            ### The first column of graphs
            html.Div(
                id= 'Visualization-C1',
                style = {
                    'width': '48%',
                    'display': 'inline-block',
                },
                children= [
                    html.Div(
                        id= 'Visualization-C1-1',
                        children= dcc.Graph(
                            id='puzzle-graph1-1',
                        ),
                    ),
                    html.Hr(),

                    html.Div(
                        id= 'Visualization-C1-2',
                        children= dcc.Graph(
                            id='puzzle-graph1-2',
                        ),
                    ),
                ]
            ),

            ### The second column of graphs
            html.Div(
                id= 'Visualization-C2',
                style={
                    'width': '48%',
                    'display': 'inline-block',
                },
                children= [
                    html.Div(
                        id='Visualization-C2-1',
                        children=dcc.Graph(
                            id='puzzle-graph2-1',
                        ),
                    ),
                    html.Hr(),

                    html.Div(
                        id='Visualization-C2-2',
                        children=dcc.Graph(
                            id='puzzle-graph2-2',
                        ),
                    ),
                ]
            )
        ]
    ),


    html.Div(
        id='Output',
        style={
            'width': '12%',
            'display': 'inline-block'
        },
        children=[
            html.H1('Information'),
            html.Div(
                id= 'Information-1'
            )
        ]
    ),
])





""""Callbacks"""
# Callback to update graph
@app.callback(
    Output('puzzle-graph1-1', 'figure'),
    [Input('puzzle-dropdown', 'value')]
)
def update_graph_img(input_value):
    return figure_layout(input_value)







# Server Things
@app.server.route('{}<image_path>.jpg'.format(imageroute))
def serve_image(image_path):
    image_name = '{}.jpg'.format(image_path)
    return flask.send_from_directory(os.getcwd() + imageroute, image_name)

if __name__ == '__main__':
    # Host doesn't matter, it just tells the app to be available in network
    app.run_server(debug=True, host= '0.0.0.0')