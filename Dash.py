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
            dcc.RadioItems(
                id='Input-add_options-metro_map'
            ),
            dcc.Dropdown(
                id='Input-add_options-gaze_color'
            ),
            dcc.Slider(
                id='Input-add_options-heatbin'
            )
        ]
    ),

    html.Div(
        id='Input-column',
        style={
            'width': '15%',
            'display': 'inline-grid',
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

            # Division for the radioitems to choose the visualization type
            html.Div(
                id= 'Input-vis_types',
                children=[
                    html.Label('Visualization Type'),
                    dcc.RadioItems(
                        id= 'Input-vis_types-types',
                        options=[
                            {'label': 'Puzzle', 'value': 'puzzle'},
                            {'label': 'Adjacency Matrix', 'value': 'adj'},
                            {'label': 'Visual Attention Map', 'value': 'mm'}
                        ],
                        labelStyle= {'display': 'inline-block',
                                     'marginRight': 80}
                    ),
                    html.Hr()
                ]
            ),

            # Division for additional options (default map options) based on the choosen visualization type
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

    # Upper division for the visualization, this division determines the borders where the graphs have to fit in
    html.Div(
        id='VisualizationHead',
        style={
            'width': '70%',
            'display': 'inline-grid',
            'marginLeft': 5,
            'marginRight': 5,
        },
        # Inner division for the visualization, all the graphs will be put in this division
        children= html.Div(
            id='Visualization',
            style= {'display': 'inline-block'},
            children= Layout.no_graphs(),
        ),
    ),

    # Division for the information output
    html.Div(
        id='Output',
        style={
            'width': '12%',
            'display': 'inline-grid',
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
     State('Input-add_options-metro_map', 'value'),
     State('Input-add_options-gaze_color', 'value'),
     State('Input-add_options-heatbin', 'value'),
     ]
)
def update_storage(n_clicks, input_puzzle,          # What puzzle to use
                   amount_panels, selected_panel,   # Panel selections
                   vis_type,                        # Type of visualization (Puzzle, Adjacency matrix, Mapping)
                   compare_method, color_adj, ordering, # For adjacency matrices
                   visual_method, color_vis_att, bin_size   # For Metro Maps
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
            graph = Graphs.get_visual_attention_map(dataset, input_puzzle, visual_method, color_vis_att, bin_size)
        elif vis_type == 'adj':
            graph = Graphs.basic_adjacency(dataset, input_puzzle, compare_method, color_adj, ordering)

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
    return [{'label': 'Panel {}'.format(i+1), 'value': i} for i in range(input_value)]

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
            html.Label('Select Puzzle or User'),
            dcc.RadioItems(
                id= 'Input-add_options-adjacency-type',
                options= [{'label': 'Puzzle', 'value': 'puzzle'},
                          {'label': 'User', 'value': 'user'}
                ]
            ),

            html.Hr(),
            # What comparison method
            html.Label('Comparison method'),
            dcc.RadioItems(
                id='Input-add_options-adjacency',
                options=[
                    {'label': 'Bounding box', 'value': 'Bounding Box'},
                    {'label': 'Euclidean distance', 'value': 'the Euclidean Distance'},
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
            html.Label('Visual Attention Options'),
            dcc.RadioItems(
                id='Input-add_options-metro_map',
                options=[
                    {'label': 'Gaze plot', 'value': 'gaze'},
                    {'label': 'Heatmap', 'value': 'attention'}
                ],
                labelStyle= {'display': 'inline-block',
                             'marginRight': 80}
            ),
            # Dropdown menu for choosing the colors for the heatmap
            html.Label('Heatmap Color'),
            dcc.Dropdown(
                id='Input-add_options-gaze_color',
                options=[
                    {'label': 'Default', 'value': 'def'},
                    {'label': 'Hot', 'value': 'hot'},
                    {'label': 'Green', 'value': 'green'},
                    {'label': 'Blue', 'value': 'blueish'},
                    {'label': 'Viridis', 'value': 'vir'},
                    {'label': 'Electric', 'value': 'elec'},
                    {'label': 'Rainbow', 'value': 'rainbow', 'disabled': 'True'},
                ],
                searchable=False,
                clearable=False,
                placeholder='Select color',
                value='blueish',
            ),
            # Slider for choosing the amount of bins for the heatmap
            html.Label('Heatmap Bin-amount'),
            dcc.Slider(
                id= 'Input-add_options-heatbin',
                included= False,
                min= 5,
                max= 50,
                value= 50,
                marks= {i: '{}'.format(i) for i in range(5, 51) if (i+10) %15 == 0},
            ),

            # Section with the dropdown menu for choosing a puzzle to visualize (including picture underneath)
            html.Hr(style= {'marginTop': 20}),
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
    '''
    Updates information screen based on user actions

    :author: Yuri Maas
    :param clickdata: The data of the point a user has clicked on
    :param hoverData: The data of the point a user is hovering (has hovered) over
    :return: Markdown object with text to show the user vital information
    '''
    if hoverData is not None:
        hover = dcc.Markdown('''
#### Hover:

Comparing scanpath of user {} with {}.
Similarity = {}
        '''.format(
            hoverData['points'][0]['y'],
            hoverData['points'][0]['x'],
            hoverData['points'][0]['z']
        ))
    else:
        hover = None

    if clickdata is not None:
        click= dcc.Markdown('''
#### Click:

Comparing scanpath of user {} with {}.
Similarity = {}
        '''.format(
            clickdata['points'][0]['y'],
            clickdata['points'][0]['x'],
            clickdata['points'][0]['z'],
        ))
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