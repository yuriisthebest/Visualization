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
defaultmap = '03_Bordeaux_S2.jpg'

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
                    opacity=0.8,
                    layer='below'
                )
            ],
            title='Graph',
            height= dataset.get_resolution_Y(new_mapname),
            width= dataset.get_resolution_X(new_mapname)
        )
    }



app = dash.Dash()

app.layout = html.Div([
    # Global Structure -> Input, Visualization, Output
    html.Div(
        id='Input',
        style={
            'width': '10%',
            'display': 'inline-block',
            'vertical-align': 'middle',
            'marginTop' : 25,
            'marginLeft' : 25,
            'marginRight': 100
        },
        children=[
            dcc.Input(id= 'my-id', value= 'initial value', type='text'),

            html.Label('Puzzle:'),
            dcc.Dropdown(
                id= 'puzzle-dropdown',
                value= defaultmap,
                options = dataset.get_puzzlenames()
            )
        ]
    ),

    html.Div(
        id='Visualization',
        style={
            'width': '60%',
            'display': 'inline-block'
        },
        children=[
            html.Div(id='my-div'),
            dcc.Graph(
                id='puzzle-graph',
            ),
        ]
    ),


    html.Div(
        id='Output',
        style={
            'width': '20%',
            'display': 'inline-block'
        },
        children=[

        ]
    ),
])


""""Callbacks"""
# Callback to tutorial
@app.callback(
    Output('my-div', 'children'),
    [Input('my-id', 'value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}'.format(input_value)


# Callback to update graph
@app.callback(
    Output('puzzle-graph', 'figure'),
    [Input('puzzle-dropdown', 'value')]
)
def update_graph_img(input_value):
    return figure_layout(input_value)


@app.server.route('{}<image_path>.jpg'.format(imageroute))
def serve_image(image_path):
    image_name = '{}.jpg'.format(image_path)
    return flask.send_from_directory(os.getcwd() + imageroute, image_name)

if __name__ == '__main__':
    app.run_server(debug=True)