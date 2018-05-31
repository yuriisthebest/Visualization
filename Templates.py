import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import flask
import os

from Storage import Data


class Layout:
    '''
    Class to store layout options for the callbacks

    :author: Yuri Maas
    '''
    @staticmethod
    def no_graphs():
        '''
        Creates a layout for the 'Plots' section for a Dash Application without any graphs

        :author: Yuri Maas
        :return: header
        '''
        return [
            html.H1('Plots'),
            html.H3('There are currently no plots,'),
            html.H3('choose options from the Input panel on the left')
        ]

    @staticmethod
    def single_graph(graph):
        '''
        Creates a layout for the 'Plots' section for a Dash Application based on an input graph

        :author: Yuri Maas
        :param graph: The graph that should be shown
        :return: The layout for the 'Plots' section of the Dash application
        '''
        return [
            html.H1('Plots'),

            html.Div(
                id= 'graph1',
                style = {
                    'width': '98%',
                    'display': 'inline-block'
                },
                children = [
                    graph
                ]
            ),
        ]

    @staticmethod
    def four_graphs(graph1, graph2, graph3, graph4):
        '''
        Creates a layout for the 'Plots' section for a Dash Application based on an input graph
        Should be called by a callback on the children of the section with id='Visualization'
        Doesn't generate any graphs

        :author: Yuri Maas
        :param list_of_graphs: An array with graphs that should be shown in the 'Plots' section
        :return: The layout for the 'Plots' section of the Dash application
        '''
        return [
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
                        id= 'graph1',
                        children = graph1
                    ),
                    html.Hr(),

                    html.Div(
                        # Graph3 because it's bottom-left
                        id= 'graph3',
                        children = graph3
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
                        # Graph 2 because it's top-right
                        id='graph2',
                        children = graph2
                    ),
                    html.Hr(),

                    html.Div(
                        id='graph4',
                        children = graph4
                    ),
                ]
            )
        ]

    @staticmethod
    def select_puzzle(dataset, initial_map= None):
        '''
        Template to create a dropdown from where a user can select a puzzle
        Also shows a miniature version underneith the dropdown

        :author: Yuri Maas
        :param dataset: The dataset used for the data and pictures
        :param initial_map: The initial map that's selected
        :return: The input layout to select a puzzle
        '''
        return [
            html.Hr(),
            html.Label('Puzzle:'),
            dcc.Dropdown(
                id='Input-add_options-puzzle_dropdown',
                value= initial_map,
                options=dataset.get_puzzlenames()
            ),
            html.Img(
                id='puzzle-image',
                style= {
                    'width': '100%'
                }
            ),
        ]


class Graphs:
    '''
    Class to store all the possible graphs in
    Definitions should return a visualization object

    :author: Yuri Maas
    '''
    @staticmethod
    def test_map(new_mapname, dataset):
        '''
        Creates a graph with a certain map as background

        :author: Yuri Maas
        :param new_mapname: The name of the puzzle to be in the graph
        :param dataset: The Class object from where to take the data
        :return: Graph object with the corresponding map in it
        '''

        imageroute = '/MetroMapsEyeTracking/stimuli/'
        return dcc.Graph(
            id= 'single-graph',
            figure = {
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
                    title='Test Graph',
                    xaxis = dict(
                        range= [0, dataset.get_resolution_X(new_mapname)]
                    ),
                    yaxis = dict(
                        range= [0, dataset.get_resolution_Y(new_mapname)]
                    ),
                    #height= dataset.get_resolution_Y(new_mapname),
                    # #width= dataset.get_resolution_X(new_mapname) - 300
                )
            }
        )