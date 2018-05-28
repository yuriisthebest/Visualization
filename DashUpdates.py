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
                id= 'Visualization-1',
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
    def multiple_graphs(list_of_graphs):
        '''
        Creates a layout for the 'Plots' section for a Dash Application based on an input graph
        Should be called by a callback on the children of the section with id='Visualization'

        :author: Yuri Maas
        :param list_of_graphs: An array with graphs that should be shown in the 'Plots' section
        :return: The layout for the 'Plots' section of the Dash application
        '''
        graph1 = list_of_graphs[0]
        graph2 = list_of_graphs[1]
        graph3 = list_of_graphs[2]
        graph4 = list_of_graphs[3]
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
                        id= 'Visualization-C1-1',
                        children= graph1
                    ),
                    html.Hr(),

                    html.Div(
                        id= 'Visualization-C1-2',
                        children= graph3 # Graph3 because it's bottom-left
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
                        children= graph2 # Graph 2 because it's top-right
                    ),
                    html.Hr(),

                    html.Div(
                        id='Visualization-C2-2',
                        children= graph4
                    ),
                ]
            )
        ]


class Graphs:
    '''
    Class to store all the possible graphs in

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
                    title='Graph',
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