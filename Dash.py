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
            html.Div(
                id= 'Graph-storage',
                children= [
                    html.Div(
                        id= 'graph1-storage',
                        children = [None]
                    ),
                    html.Div(
                        id= 'graph2-storage',
                        children = [None]
                    ),
                    html.Div(
                        id= 'graph3-storage',
                        children = [None]
                    ),
                    html.Div(
                        id= 'graph4-storage',
                        children = [None]
                    ),
                ]
            )
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
                            {'label': 'Adjacency Matrix', 'value': 0},
                            {'label': 'Metro Map', 'value': 1}
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
# 2 Callbacks to update the visualization plot
'''
@app.callback(
    Output('Visualization', 'children'),
    [Input('Submit', 'n_clicks')],
     state = [State('Input-add_options-puzzle_dropdown', 'value'),
              State('Input-panels-dropdown', 'value'),
              State('Input-panels-panels', 'value'),
              State('Graph-storage', 'children')]
)
def update_visualization(n_clicks, input_puzzle, amount_panels, panel, current_list):
    
    Updates the visualization based on the given parameters

    :author: Yuri Maas
    :param n_clicks: Usefull to check whether the button has been pressed, no other uses
    :param input_puzzle: The name of the new map
    :param amount_panels: The total amount of requested panels
    :param panel: The panel to update
    :return: Layout with a single graph
    
    if amount_panels == 1:
        return Layout.single_graph(
            Graphs.test_map(input_puzzle, dataset)
        )
    if amount_panels == 4:
        list_of_graphs = current_list
        list_of_graphs[panel] = Graphs.test_map(input_puzzle, dataset)
        return Layout.multiple_graphs(
            list_of_graphs
        )
    return Layout.no_graphs()


@app.callback(
    Output('Graph-storage', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-dropdown', 'value'),
     State('Input-panels-panels', 'value'),
     State('Graph-storage', 'children')]
)
def update_graph_storage(n_clicks, input_puzzle, amount_panels, panel, current_list):
    if panel == None:
        return current_list
    new_list = current_list
    new_list[panel] = Graphs.test_map(input_puzzle, dataset)
    return new_list

@app.callback(
    Output('Visualization', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-dropdown', 'value'),
     State('Input-panels-panels', 'value'),
     State('Graph-storage', 'children')]
)
def update_visualization(n_clicks, input_puzzle, amount_panels, panel, current_list):
    if amount_panels == 1:
        return Layout.single_graph(
            Graphs.test_map(input_puzzle, dataset)
        )
    if amount_panels == 4:
        list_of_graphs = current_list
        list_of_graphs[panel] = Graphs.test_map(input_puzzle, dataset)
        return Layout.multiple_graphs(
            list_of_graphs
        )
    return Layout.no_graphs()

# Changes the layout based on the amount of desired panels
@app.callback(
    Output('Visualization', 'children'),
    [Input('Input-panels-dropdown', 'value')]
)
def update_layout(amount_panels):
    if amount_panels == 1:
        return Layout.single_graph()
    if amount_panels == 4:
        return Layout.four_graphs()
    return Layout.no_graphs()


@app.callback(
    Output('Visualization', 'children'),
    [Input('graph1-storage', 'children'),
     Input('graph2-storage', 'children'),
     Input('graph3-storage', 'children'),
     Input('graph4-storage', 'children')],
    [State('Input-panels-dropdown', 'value')]
)
def update_visualization(graph1, graph2, graph3, graph4, amount_panels):
    if amount_panels == 1:
        return Layout.single_graph(
            graph1
        )
    if amount_panels == 4:
        return Layout.four_graphs(
            [graph1, graph2, graph3, graph4]
        )
    return Layout.no_graphs()


# Change graph 1
@app.callback(
    Output('graph1-storage', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-panels', 'value')]
)
def update_graph1_storage(n_clicks, input_puzzle, panel):
    if panel == 0:
        return [Graphs.test_map(input_puzzle, dataset)]


# Change graph 2
@app.callback(
    Output('graph2-storage', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-panels', 'value')]
)
def update_graph2_storage(n_clicks, input_puzzle, panel):
    if panel == 1:
        return [Graphs.test_map(input_puzzle, dataset)]


# Change graph 3
@app.callback(
    Output('graph3-storage', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-panels', 'value')]
)
def update_graph3_storage(n_clicks, input_puzzle, panel):
    if panel == 2:
        return [Graphs.test_map(input_puzzle, dataset)]


# Change graph 4
@app.callback(
    Output('graph4-storage', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-panels', 'value')]
)
def update_graph4_storage(n_clicks, input_puzzle, panel):
    if panel == 3:
        return [Graphs.test_map(input_puzzle, dataset)]
'''

@app.callback(
    Output('Visualization', 'children'),
    [Input('Submit', 'n_clicks')],
    [State('Input-add_options-puzzle_dropdown', 'value'),
     State('Input-panels-dropdown', 'value'),
     State('Input-panels-panels', 'value')]
)
def update_storage(n_clicks, input_puzzle, amount_panels, selected_panel):
    if selected_panel is not None and input_puzzle is not None:
        plots.reset_graph(selected_panel)
        plots.set_graph(selected_panel,
                        Graphs.test_map(input_puzzle, dataset))

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
    # 0 = Adjacency Matrix
    # 1 = Metro Map
    if input_type == 0:
        return [
            # Choose Puzzle, Choose Adjacency matrix type
            dcc.RadioItems(
                id='Input-add_options-adjacency',
                options=[

                ]
            ),
            html.Div(
                id= 'Input-select_puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]

    if input_type == 1:
        return [
            # Choose puzzle, Choose map overlay
            dcc.RadioItems(
                id='Input-add_options-metro_map',
                options=[
                    {'label': 'Gaze plot', 'value': 0},
                    {'label': 'Attention map', 'value': 1}
                ],
                labelStyle= {'display': 'inline-block',
                             'marginRight': 80}
            ),
            html.Div(
                id= 'Input-select_puzzle',
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




# Server and Image things
@app.server.route('{}<image_path>.jpg'.format(imageroute))
def serve_image(image_path):
    image_name = '{}.jpg'.format(image_path)
    return flask.send_from_directory(os.getcwd() + imageroute, image_name)

if __name__ == '__main__':
    # Host doesn't matter, it just tells the app to be available in network
    app.run_server(debug=True, host= '0.0.0.0')