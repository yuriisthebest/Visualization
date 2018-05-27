import pandas as pd


class Layout:
    '''
    Class to store layout options for the callbacks

    :author: Yuri Maas
    '''
    def no_graphs(self):
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

    def single_graph(self, graph):
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

    def multiple_graphs(self, list_of_graphs):
        '''
        Creates a layout for the 'Plots' section for a Dash Application based on an input graph
        Should be called by a callback on the children of the section with id='Visualization'

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

class Graphs:
    '''
    Class to store all the possible graphs in

    :author: Yuri Maas
    '''
