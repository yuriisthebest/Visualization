# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import flask
import os
import time

# My packages
from Storage import Data, Current_Graphs
from Templates import Graphs, Layout
dataset = Data()
plots = Current_Graphs()

# Constants
imageroute = '/MetroMapsEyeTracking/stimuli/'
defaultmap = '03_Bordeaux_S1.jpg'


app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

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
            # These are hidden, necessary for error prevention
            dcc.RadioItems(
                id= 'Input-add_options-adjacency',
            ),
            dcc.Dropdown(
                id='Input-add_options-adjacency_color'
            ),
            dcc.Dropdown(
                id='Input-add_options-adjacency_order'
            ),
        ]
    ),

    html.Div(
        id='Input-column',
        style={
            'width': '15%',
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
                    # Visualize-Logo
                    html.Hr(),
                    html.Img(
                        id= 'Company logo',
                        src= imageroute + 'VisualEyes.jpg',
                        title= 'Visual-Eyes\nJust let the user do it',
                        style={
                            'width': '100%'
                        },
                    ),

                    # Submit button
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
                        placeholder= 'Select an amount of panels',
                        #value= 4
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
                            {'label': 'Puzzle', 'value': 'puzzle'},
                            {'label': 'Adjacency Matrix', 'value': 'adj'},
                            {'label': 'Metro Map', 'value': 'mm'}
                        ],
                        labelStyle= {'display': 'inline-block',
                                     'marginRight': 80}
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
            html.Div(
                id= 'Input-puzzle (WIP',
            )
        ]
    ),


    html.Div(
        id='Visualization',
        style={
            'width': '70%',
            'display': 'inline-block',
            'marginLeft': 5,
            'marginRight': 5
        },
        children= Layout.no_graphs(),
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
            ),
        ]
    ),
])





"""Callbacks"""
# Callback to update the visualization
@app.callback(
    Output('Visualization', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-dropdown', 'value'),
     State('Input-panels-panels', 'value'),
     State('Input-vis_types-types', 'value'),
     State('Input-add_options-adjacency', 'value'),
     State('Input-add_options-adjacency_color', 'value'),
     State('Input-add_options-adjacency_order', 'value'),
     ]
)
def update_storage(n_clicks, input_puzzle,          # What puzzle to use
                   amount_panels, selected_panel,   # Panel selections
                   vis_type,                        # Type of visualization (Puzzle, Adjacency matrix, Mapping)
                   compare_method, color, ordering  # For adjacency matrices
                   ):
    '''
    Updates the visualization based on the input parameters

    :author: Yuri Maas
    :param n_clicks: number of times the button has been clicked, irrelevant, only used to detect change
    :param input_puzzle: The (raw) name of the puzzle to use
    :param amount_panels: The amount of plots the visualization has to use
    :param selected_panel: Which panel to modify
    :param vis_type: The type of visualization to put ni the selected panel
    :param compare_method: In case of adjacency matrix, the comparison method to use
    :param color: In case of adjacency matrix, the color to use
    :param ordering: In case of adjacency matrix, the sorting algorithm use to order the matrix
    :return: A layout for the visualization with a certain amount of determined plots
    '''
    if selected_panel is not None and input_puzzle is not None:
        plots.reset_graph(selected_panel)
        time.sleep(0.05)

        graph = None
        if vis_type == 'puzzle':
            graph = Graphs.puzzle_image(input_puzzle)
        elif vis_type == 'mm':
            graph = Graphs.test_map(input_puzzle, dataset)
        elif vis_type == 'adj':
            graph = Graphs.basic_adjacency(dataset, input_puzzle, compare_method, color, ordering)

        plots.set_graph(selected_panel,
                        graph)

    time.sleep(0.05)
    if amount_panels == 1:
        return Layout.single_graph(
            plots.get_graph(0)
        )

    if amount_panels == 4:
        return Layout.four_graphs(
            plots.get_graph(0),
            plots.get_graph(1),
            plots.get_graph(2),
            plots.get_graph(3)
        )

    for i in range(4):
        plots.reset_graph(i)
    return Layout.no_graphs()



# Callback to change the amount of panels based on the panel dropdown
@app.callback(
    Output('Input-panels-panels', 'options'),
    [Input('Input-panels-dropdown', 'value')]
)
def update_panels(input_value):
    '''
    Adds panel RadioItems equal to the desired amount of visualization panels

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
def update_visualization_options(input_type):
    '''
    Add additional options for the visualization types

    :author: Yuri Maas
    :param input_type: The type of visualization that's desired
    :return: Additional options
    '''
    # adj = Adjacency Matrix
    # mm = Metro Map
    # puzzle = Puzzle
    if input_type == 'adj':
        return [
            # What comparison method
            html.Label('Comparison method'),
            dcc.RadioItems(
                id='Input-add_options-adjacency',
                options=[
                    {'label': 'Test comparison', 'value': 'test'},
                    {'label': 'Bounding box', 'value': 'bound'},
                    {'label': 'Euclidean distance', 'value': 'euc'},
                ],
                labelStyle={'display': 'inline-block',
                            'marginRight': 80}
            ),

            # What colorscale the adjacency matrix should use
            html.Label('Color'),
            dcc.Dropdown(
                id='Input-add_options-adjacency_color',
                options=[
                    {'label': 'Default', 'value': 'def'},
                    {'label': 'Hot', 'value': 'hot'},
                    {'label': 'Green', 'value': 'green'},
                    {'label': 'Viridis', 'value': 'vir'},
                    {'label': 'Electric', 'value': 'elec', 'disabled': 'True'},
                    {'label': 'Rainbow', 'value': 'rainbow'},
                ],
                searchable= False,
                clearable= False,
                placeholder= 'Select color',
                value= 'def',
            ),

            # What ordering method to use
            html.Label('Ordering'),
            dcc.Dropdown(
                id='Input-add_options-adjacency_order',
                options=[
                    {'label': 'No ordering', 'value': 'no'},
                    {'label': 'Alphabetical ordering', 'value': 'alphabet'},
                ],
                searchable= False,
                clearable= False,
                value= 'no',
            ),

            # The puzzle selection
            html.Hr(),
            html.Div(
                id= 'Input-select_puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]

    if input_type == 'mm':
        return [
            # Choose puzzle, Choose map overlay
            dcc.RadioItems(
                id='Input-add_options-metro_map',
                options=[
                    {'label': 'Gaze plot', 'value': 'gaze'},
                    {'label': 'Attention map', 'value': 'attention'}
                ],
                labelStyle= {'display': 'inline-block',
                             'marginRight': 80}
            ),
            html.Hr(),
            html.Div(
                id= 'Input-select_puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]

    if input_type == 'puzzle':
        return [
            html.Div(
                id= 'Input-select-puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]

# Callback that changes the puzzle shown when selecting a panel
@app.callback(
    Output('puzzle-image', 'src'),
    [Input('Input-add_options-puzzle_dropdown', 'value')]
)
def update_map_image(input_puzzle):
    if input_puzzle is None:
        return None
    return imageroute + input_puzzle



# Callback to select data at hover and show it as information
@app.callback(
    Output('Information-1', 'children'),
    [Input('adjacency-matrix', 'clickData'),
     Input('adjacency-matrix', 'hoverData')]
)
def display_click_data(clickdata, hoverData):
    if hoverData is not None:
        hover = html.P('Hover data:\nComparing scanpath of user {} with {}.\nTheir similarity = {}'.format(
            hoverData['points'][0]['y'],
            hoverData['points'][0]['x'],
            hoverData['points'][0]['z']))
    else:
        hover = None

    if clickdata is not None:
        click = html.P('Click data:\nComparing scanpath of user {} with {}.\nTheir similarity = {}'.format(
            clickdata['points'][0]['y'],
            clickdata['points'][0]['x'],
            clickdata['points'][0]['z']))
    else:
        click = None

    return [hover, click]




# Server and Image things
@app.server.route('{}<image_path>.jpg'.format(imageroute))
def serve_image(image_path):
    image_name = '{}.jpg'.format(image_path)
    return flask.send_from_directory(os.getcwd() + imageroute, image_name)

if __name__ == '__main__':
    # Host doesn't matter, it just tells the app to be available in network
    app.run_server(debug=True, host= '0.0.0.0')