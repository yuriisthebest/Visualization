import pandas as pd
import numpy as np
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import flask
import os
import matplotlib.pyplot as plt
from PIL import Image
import sys
from io import BytesIO
import base64

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
    Class to store all the possible plots in
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

    @staticmethod
    def puzzle_image(puzzle):
        '''
        Finds and shows the image of a certain puzzle

        :author: Yuri Maas
        :param puzzle: The name of the puzzle to show in the plot
        :return: Image object with the puzzle image
        '''
        return html.Img(
            id = 'puzzle-plot',
            style= {
                'width': '100%'
            },
            src= '/MetroMapsEyeTracking/stimuli/' + puzzle
        )

    @staticmethod
    def basic_adjacency(dataset, new_mapname, compare_method, colortype, ordering):
        '''
        Creates an adjacency matrix graph for the Plots panel

        :author: Yuri Maas
        :param dataset: The data to use to create the adjacency matrix
        :param new_mapname: The puzzle to use
        :param compare_method: Which method to use to grade 2 paths on
        :param colortype: The color the heatmap should be
        :param ordering: The reorder algorithm that should be used
        :return: Heatmap object which shows the adjacency matrix for all paths of a certain puzzle
        '''
        # Get the fixation data for the puzzle
        all_paths = dataset.get_puzzle_data(new_mapname)
        all_users = [all_paths[i]['user'].unique()[0] for i in range(len(all_paths))]
        # Set-up a matrix with only zeros to fill in
        matrix = np.zeros((len(all_users), len(all_users)))

        for i in range(len(all_users)):
            path1 = all_paths[i]
            for j in range(i, len(all_users)):
                path2 = all_paths[j]
                similarity = Graphs.compare(compare_method, path1, path2)
                matrix[i, j] = similarity
                matrix[j, i] = similarity

        # Order the matrix
        #if ordering == 'alphabet':


        # Determine the colorscale
        colordict = {
            'def': 'RdBu',
            'hot': 'Hot',
            'green': 'Greens',
            'vir': 'Viridis',
            'elec': 'Electric',
            'rainbow': 'Rainbow',
        }
        return dcc.Graph(
            id= 'adjacency-matrix',
            clear_on_unhover= True,
            config= {
                'modeBarButtonsToRemove': [
                    'autoScale2d',
                    'zoomIn2d',
                    'zoomOut2d',
                    'hoverClosestCartesian',
                    'hoverCompareCartesian',
                    'toggleSpikelines',
                    'sendDataToCloud'],
            },
            figure= {
                'data': [
                    {
                        'z': matrix,
                        'x': all_users,
                        'y': all_users,
                        'type': 'heatmap',
                        'colorscale': colordict[colortype],
                    }
                ],
                'layout': go.Layout(
                    title= 'Adjacency Matrix of puzzle: {}'.format(new_mapname[3:-4]),
                    yaxis= dict(autorange= 'reversed')
                )
            }
        )

    @staticmethod
    def compare(method, path1, path2):
        '''
        Calls the method to determine the similarity between path1 and path2

        :author: Yuri Maas
        :param method: The method to determine similarity
        :param path1: Path to compare with path2
        :param path2: Path to compare with path1
        :return: A value that resembles the similarity between path1 and path2
        '''
        if method == 'bound':
            return Graphs.adjcompare_bounding_box(path1, path2)
        if method == 'euc':
            return Graphs.adjcompare_euc_dist(path1, path2)
        return Graphs.adjcompare_random()

    @staticmethod
    def adjcompare_random():
        '''
        Returns a value between 0 and 1 randomly

        :author: Yuri Maas
        :param path1: The scanpath to compare to path2
        :param path2: The scanptah to compare to path1
        :return: value > 0 && value < 1
        '''
        return 0.5 * random.randint(0, 1) + 0.25 * random.randint(0, 1) + 0.25 * random.randint(0, 1)

    @staticmethod
    def adjcompare_bounding_box(path1, path2):
        '''
        Calculates the bounding box overlap between two scanpaths

        :author: Yuri Maas
        :param path1: The scanpath (in DataFrame) to compare to path2
        :param path2: The scanpath (in DataFrame) to compare to path1
        :return: A similarity value between 0 and 1
        '''
        xmax_1 = max(path1['MappedFixationPointX'])
        xmin_1 = min(path1['MappedFixationPointX'])
        ymax_1 = max(path1['MappedFixationPointY'])
        ymin_1 = min(path1['MappedFixationPointY'])

        xmax_2 = max(path2['MappedFixationPointX'])
        xmin_2 = min(path2['MappedFixationPointX'])
        ymax_2 = max(path2['MappedFixationPointY'])
        ymin_2 = min(path2['MappedFixationPointY'])

        xmax_box = min(xmax_1, xmax_2)
        xmin_box = max(xmin_1, xmin_2)
        ymax_box = min(ymax_1, ymax_2)
        ymin_box = max(ymin_1, ymin_2)
        dx = xmax_box - xmin_box
        dy = ymax_box - ymin_box
        if dx >= 0 and dy >= 0:
            overlap_area = dx * dy
            area_1 = (xmax_1 - xmin_1) * (ymax_1 - ymin_1)
            area_2 = (xmax_2 - xmin_2) * (ymax_2 - ymin_2)
            # The total area of 2 rectangles is the area of 1 + (The area of the other - the overlapping part)
            totalarea = area_1 + area_2 - overlap_area
            return overlap_area / totalarea
        return 0

    @staticmethod
    def adjcompare_bounding_box_dep(path1, path2):
        '''

        :author: Maaike? Finish this
        :param path1:
        :param path2:
        :return:
        '''
        Rect = namedtuple('Rectangle', 'xmin ymin xmax ymax')
        xmin_1 = min([path1[i][5] for i in range(len(path1))])
        xmax_1 = max([path1[i][5] for i in range(len(path1))])
        ymin_1 = min([path1[i][6] for i in range(len(path1))])
        ymax_1 = max([path1[i][6] for i in range(len(path1))])
        R1 = Rect(xmin_1, ymin_1, xmax_1, ymax_1)

        xmin_2 = min([path2[i][5] for i in range(len(path2))])
        xmax_2 = max([path2[i][5] for i in range(len(path2))])
        ymin_2 = min([path2[i][6] for i in range(len(path2))])
        ymax_2 = max([path2[i][6] for i in range(len(path2))])
        R2 = Rect(xmin_2, ymin_2, xmax_2, ymax_2)

        dx = min(R1.xmax, R2.xmax) - max(R1.xmin, R2.xmin)
        dy = min(R1.ymax, R2.ymax) - max(R1.ymin, R2.ymin)

        if (dx >= 0) and (dy >= 0):
            area = dx * dy
            area_1 = (R1.xmax - R1.xmin) * (R1.ymax - R1.ymin)
            area_2 = (R2.xmax - R2.xmin) * (R2.ymax - R2.ymin)
            total_area = area_1 + area_2
            return area / total_area
        else:
            return 0

    @staticmethod
    def adjcompare_euc_dist(path1, path2):
        '''

        :author: Annelies? Finish this
        :param path1:
        :param path2:
        :return:
        '''
        x1 = np.array(np.matlib.repmat(path1[:, 4].reshape((len(path1), 1)), 1, len(path2)))
        x2 = np.array(np.matlib.repmat(path2[:, 4].reshape((1, len(path2))), len(path1), 1))

        y1 = np.array(np.matlib.repmat(path1[:, 5].reshape((len(path1), 1)), 1, len(path2)))
        y2 = np.array(np.matlib.repmat(path2[:, 5].reshape((1, len(path2))), len(path1), 1))

        distx = np.power(x1 - x2, 2)
        disty = np.power(y1 - y2, 2)

        Euc_dist = np.array(np.power(distx + disty, 0.5))
        Euc_dist_colmin = np.amin(Euc_dist, axis=0)  # minimum distances for sequence A
        Euc_dist_rowmin = np.amin(Euc_dist, axis=1)  # minimum distances for sequence B

        Euc_dist_tot = np.sum(Euc_dist_colmin) + np.sum(Euc_dist_rowmin)
        map_dimensions = np.array([1920, 1200])
        m = np.power(np.power(map_dimensions[0], 2) + np.power(map_dimensions[1], 2),
                     0.5)  # calculate maximum possible distance!
        Euc_dist_tot_norm = 1 / ((len(Euc_dist_colmin) + len(Euc_dist_rowmin)) * m) * Euc_dist_tot

        return Euc_dist_tot_norm


    @staticmethod
    def get_visual_attention_map(stimuli, dataset):
        """
        gets the image of a certain stimuli
        :author Maaike van Delft
        :param the stimuli where we want the image from

        """

        df = dataset.get_puzzle_data(stimuli)

        #Get x and y cooridnates
        dfx = df[:, 4]
        dfy = df[:, 5]
        x = np.array(dfx, dtype=float)
        y = np.array(dfy, dtype=float)


        script_dir = sys.path[0]
        image_path = os.path.join(script_dir, 'MetroMapsEyeTracking/stimuli/' + stimuli)
        img = Image.open(image_path)
        plt.imshow(img)

        implot = plt.imshow(img)
        heatmap_z, xedges, yedges = np.histogram2d(x, y, bins=30)
        extent_2 = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        plt.plot()
        plt.imshow(heatmap_z.T, extent=extent_2, origin='lower', camp='inferno', alpha=0.5)
        plt.colorbar()

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        return base64.b64encode(figfile.getvalue())


    @staticmethod
    def gaze_plot(dataset, stimuli, color):
        data = dataset.get_puzzle_data()
        image_file = '/MetroMapsEyeTracking/stimuli/' + stimuli
        img = Image.open(image_file, )
        x_gaze = np.array(data['MappedFixationPointX'], dtype=float)
        y_gaze = np.array(data['MappedFixationPointY'], dtype=float)
        #fixationduration
        d_gaze = np.array(data['FixationDuration'], dtype=float)
        plt.imshow(img)
        # put a red dot, size 40, at 2 locations:
        #color options as many as there are users. Take red, deepskyblue, lawngreen, blue, darkviolet, fuchsia, maroon, darkorange, darkgreen, saddlebrown, mediumspringgreen, slategrey.

        plt.scatter(x_gaze , y_gaze , c= color, marker='o', alpha=0.4, s=d_gaze, zorder=2)
        plt.plot(x_gaze, y_gaze, color, alpha=0.5)
        gaze_plot = plt.axis('off')

        return gaze_plot