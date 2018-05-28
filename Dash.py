# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import flask
import os

# My packages
from Storage import Data
from DashUpdates import Graphs, Layout
dataset = Data()


# Constants
imageroute = '/MetroMapsEyeTracking/stimuli/'
defaultmap = '03_Bordeaux_S1.jpg'



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

    # Store data
    html.Div(
        id= 'hidden',
        style= {'display': 'none'},
        children= [
            html.Div(),
            html.Div()
        ]
    ),

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
                    html.Hr(),
                    html.Button(
                        'Submit Graph',
                        id= 'Submit',
                        title= 'Press this button to '
                               'submit the choosen options to \'Plots\'',
                        style= {
                            
                        }
                    ),
                    html.Hr()
                ]
            ),

            html.Div(
                id= 'Input-panels',
                children=[
                    dcc.Dropdown(
                        id= 'Input-panels-dropdown',
                        options= [
                            {'label': '1 Panel', 'value': 1},
                            {'label': '4 Panels', 'value': 4}
                        ],
                        searchable= False,
                        placeholder= 'Select an amount of panels'
                    ),

                    dcc.RadioItems(
                        id= 'Input-panels-panels',
                        options=[
                            {'label': 'Panel 1', 'value': 0},
                            {'label': 'Panel 2', 'value': 1},
                            {'label': 'Panel 3', 'value': 2},
                            {'label': 'Panel 4', 'value': 3}
                        ],
                        labelStyle= {'display': 'inline-block',
                                     'marginRight': 60}
                    ),
                    html.Hr()
                ]
            ),

            html.Div(
                id= 'Input-vis_types',
                children=[
                    dcc.RadioItems(
                        id= 'Input-vis_types-types',
                        options=[
                            {'label': 'Adjacency Matrix', 'value': 0},
                            {'label': 'Metro Map', 'value': 1}
                        ],
                        labelStyle= {'display': 'inline-block'}
                    ),
                    html.Hr()
                ]
            ),

            html.Div(
                id= 'Input-add_options',
                children= [
                    html.Label('Puzzle:'),
                    dcc.Dropdown(
                        id='Input-add_options-puzzle_dropdown',
                        value=defaultmap,
                        options=dataset.get_puzzlenames()
                    ),
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





"""Callbacks"""
# Callback to update the visualization plot
@app.callback(
    Output('Visualization', 'children'),
    [Input('Submit', 'n_clicks')],
     state = [State('Input-add_options-puzzle_dropdown', 'value'),
              State('Input-panels-dropdown', 'value'),
              State('Input-panels-panels', 'value')]
)
def update_visualization(n_clicks, input_puzzle, amount_panels, panel):
    '''
    Updates the visualization based on the given parameters

    :author: Yuri Maas
    :param n_clicks: Usefull to check whether the button has been pressed, no other uses
    :param input_puzzle: The name of the new map
    :param amount_panels: The total amount of requested panels
    :param panel: The panel to update
    :return: Layout with a single graph
    '''
    if amount_panels == 1:
        return Layout.single_graph(
            Graphs.test_map(input_puzzle, dataset)
        )
    if amount_panels == 4:
        list_of_graphs = [None, None, None, None]
        list_of_graphs[panel] = Graphs.test_map(input_puzzle, dataset)
        return Layout.multiple_graphs(
            list_of_graphs
        )
    return Layout.no_graphs()


# Callback to change the amount of panels based on the panel dropdown
@app.callback(
    Output('Input-panels-panels', 'options'),
    [Input('Input-panels-dropdown', 'value')]
)
def update_options(input_value):
    '''
    Adds RadioItems equal to the desired amount of visualization panels

    :author: Yuri Maas
    :param input_value: Amount of desired panels
    :return: #input_value RadioItem options
    '''
    if input_value == None:
        return []
    options = [{'label': 'Panel {}'.format(i+1), 'value': i} for i in range(input_value)]
    return options

# Add additional options once a visualization type has been chosen
@app.callback(
    Output('Input-add_options', 'children'),
    [Input('Input-vis_types-types', 'value')]
)
def update_additional_options(input_type):

    # 0 = Adjacency Matrix
    # 1 = Metro Map
    if input_type == 0:
        return [
            # Choose Puzzle, Choose Adjacency matrix type
            html.Label('Puzzle:'),
            dcc.Dropdown(
                id='Input-add_options-puzzle_dropdown',
                value=defaultmap,
                options=dataset.get_puzzlenames()
            ),
            dcc.RadioItems(
                id='Input-add_options-adjacency',
                options=[

                ]
            )
        ]

    if input_type == 1:
        return [
            # Choose puzzle, Choose map overlay
            html.Label('Puzzle:'),
            dcc.Dropdown(
                id='Input-add_options-puzzle_dropdown',
                value=defaultmap,
                options=dataset.get_puzzlenames()
            ),
            dcc.RadioItems(
                id='Input-add_options-metro_map',
                options=[
                    {'label': 'Gaze plot', 'value': 0},
                    {'label': 'Attention map', 'value': 1}
                ],
                labelStyle= {'display': 'inline-block',
                             'marginRight': 20}
            ),
        ]



# Server Things
@app.server.route('{}<image_path>.jpg'.format(imageroute))
def serve_image(image_path):
    image_name = '{}.jpg'.format(image_path)
    return flask.send_from_directory(os.getcwd() + imageroute, image_name)

if __name__ == '__main__':
    # Host doesn't matter, it just tells the app to be available in network
    app.run_server(debug=True, host= '0.0.0.0')