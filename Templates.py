import numpy as np
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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
                placeholder= 'Select a puzzle',
                options=dataset.get_puzzlenames(),
            ),
            html.Img(
                id='puzzle-image',
                style= {
                    'width': '100%'
                }
            ),
        ]

    @staticmethod
    def puzzle_options(dataset):
        return [
            html.Div(
                id= 'Input-select-puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]

    @staticmethod
    def visual_attention_options(dataset):
        return [
            # Choose puzzle, Choose map overlay
            html.Label('Visual Attention Options'),
            dcc.RadioItems(
                id='Input-add_options-metro_map',
                options=[
                    {'label': 'Gaze plot', 'value': 'gaze'},
                    {'label': 'Heatmap', 'value': 'attention'}
                ],
                labelStyle={'display': 'inline-block',
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
                id='Input-add_options-heatbin',
                included=False,
                min=5,
                max=50,
                value=20,
                marks={i: '{}'.format(i) for i in range(5, 51) if (i + 10) % 15 == 0},
            ),

            # Section with the dropdown menu for choosing a puzzle to visualize (including picture underneath)
            html.Hr(style={'marginTop': 20}),
            html.Div(
                id='Input-select_puzzle',
                children=Layout.select_puzzle(dataset)
            )
        ]

    @staticmethod
    def adjacency_options(dataset):
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

            # The puzzle selection (and user if choosen)
            html.Hr(),
            html.Div(
                id= 'Input-select_user',
            ),
            html.Div(
                id= 'Input-select_puzzle',
                children= Layout.select_puzzle(dataset)
            )
        ]


class Graphs:
    '''
    Class to store all the possible plots in
    Definitions should return a visualization object

    :author: Yuri Maas
    '''
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

    ############### Start Adjacency Matrix ######################################################
    @staticmethod
    def basic_adjacency(dataset, new_mapname, adj_type, compare_method, colortype, ordering, input_user):
        '''
        Creates an adjacency matrix graph for the Plots panel

        :author: Yuri Maas
        :param dataset: The data to use to create the adjacency matrix
        :param new_mapname: The puzzle to use
        :param adj_type: The type of adjacency matrix (Puzzle or User)
        :param compare_method: Which method to use to grade 2 paths on
        :param colortype: The color the heatmap should be
        :param ordering: The reorder algorithm that should be used
        :return: Heatmap object which shows the adjacency matrix for all paths of a certain puzzle
        '''
        # Get the fixation data for the puzzle
        if adj_type == 'puzzle':
            all_paths = dataset.get_puzzle_data(new_mapname)
            labels = [all_paths[i]['user'].unique()[0] for i in range(len(all_paths))]
        elif adj_type == 'user':
            all_paths = dataset.get_subscanpaths(new_mapname, input_user)
            labels = ['Length: {} from {}'.format(len(scan), scan.index[0]) for scan in all_paths]

        # Set-up a matrix with only zeros to fill in
        matrix = np.zeros((len(labels), len(labels)))

        for i in range(len(labels)):
            path1 = all_paths[i]
            for j in range(i, len(labels)):
                path2 = all_paths[j]
                similarity = np.round(Graphs.compare(compare_method, path1, path2), 4)
                matrix[i, j] = similarity
                matrix[j, i] = similarity

        # Order the matrix
        if ordering == 'alphabet':
            labels, matrix = Graphs.reorder_alphabet(labels, matrix, adj_type)

        # Determine the hovertext and colorscale
        text= []
        for x in range(len(all_paths)):
            midterm= []
            for y in range(len(all_paths)):
                if adj_type == 'puzzle':
                    midterm.append('Similarity of user {} and {} = {}'.format(
                        labels[x],
                        labels[y],
                        matrix[x, y],
                    ))
                elif adj_type == 'user':
                    midterm.append('Similarity of scanpath with {} and scanpath with {} = {}'.format(
                        labels[x],
                        labels[y],
                        matrix[x, y],
                    ))
                text.append(midterm)

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
                        'x': labels,
                        'y': labels,
                        'type': 'heatmap',
                        'colorscale': colordict[colortype],
                        'colorbar': {
                            'showticklabels': False,
                            'title': 'Low <--- (Similarity) ---> High',
                            'titleside': 'right',
                        },
                        'hoverinfo': 'text',
                        'text': text
                    }
                ],
                'layout': go.Layout(
                    title= 'Adjacency Matrix of {} based on {}'.format(new_mapname[3:-4], compare_method),
                    yaxis= dict(autorange= 'reversed')
                )
            }
        )

    @staticmethod
    def reorder_alphabet(labels, matrix, adj_type):
        '''
        Reorders the rows and columns of the adjacency matrix so that the labels are in alphabetical order

        :author: Yuri Maas
        :param labels: The labels of the axis of the matrix
        :param matrix: The matrix to reorder
        :return: The labels in alphabetical order with the associated matrix
        '''
        # Function to go from the user name (p#) to an interger for sorting purposes
        if adj_type == 'puzzle':
            def remove_p(element):
                return int(element.strip('p'))
        else:
            def remove_p(element):
                return element

        # Create an alphabetically sorted list of the users
        user_sort_index= sorted(labels, key=remove_p)
        # Check for all users what index they have in the new sorted list and make a list of those indexes
        sort_index= [index
                     for user in user_sort_index
                     for index in range(len(user_sort_index))
                     if user == labels[index]]
        sort_matrix= np.zeros((len(sort_index), len(sort_index)))
        # Create an elementary matrix that can reorder the columns based on the sort_index
        for i in range(len(sort_index)):
            sort_matrix[sort_index[i], i]= 1

        # Sort the labels according to the sort_index
        new_labels= [labels[i] for i in sort_index]

        # Sort the matrix (matrix[sort_index] reorder the rows of the matrix)
        # Multiplying the row-sortedmatrix with the elementmatrix to reorder the columns will give the sorted matrix
        new_matrix= np.matmul(matrix[sort_index], sort_matrix)
        return new_labels, new_matrix


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
        if method == 'Bounding Box':
            return Graphs.adjcompare_bounding_box(path1, path2)
        if method == 'the Euclidean Distance':
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
            if totalarea == 0:
                return 0
            return overlap_area / totalarea
        return 0

    @staticmethod
    def adjcompare_euc_dist(path1, path2, max_X = 1920, max_Y = 1200):
        '''
        Calculates the similarity between 2 scanpaths based on the euclidean distance between the two

        :author: Annelies van de Wetering
        :param path1: The scanpath (in DataFrame) to compare to path2
        :param path2: The scanpath (in DataFrame) to compare to path1
        :return: A similarity value between 0 and 1
        '''
        x1 = np.array(path1['MappedFixationPointX'], dtype=float)
        y1 = np.array(path1['MappedFixationPointY'], dtype=float)
        x2 = np.array(path2['MappedFixationPointX'], dtype=float)
        y2 = np.array(path2['MappedFixationPointY'], dtype=float)

        distx = np.power(x1[:, None] - x2, 2)
        disty = np.power(y1[:, None] - y2, 2)

        Euc_dist = np.array(np.power(distx + disty, 0.5))
        Euc_dist_colmin = np.amin(Euc_dist, axis=0)  # minimum distances for sequence A
        Euc_dist_rowmin = np.amin(Euc_dist, axis=1)  # minimum distances for sequence B

        Euc_dist_tot = np.sum(Euc_dist_colmin) + np.sum(Euc_dist_rowmin)
        map_dimensions = np.array([max_X, max_Y])  # the real dimensions of a map should be added
        m = np.power(np.power(map_dimensions[0], 2) + np.power(map_dimensions[1], 2),
                     0.5)  # calculate maximum possible distance!
        Euc_dist_tot_norm = 1 / ((len(Euc_dist_colmin) + len(Euc_dist_rowmin)) * m) * Euc_dist_tot

        return 1 - Euc_dist_tot_norm
############## End of Adjacency Matrix ############################################################
############## Start of Visual Attention Map ######################################################
    @staticmethod
    def get_visual_attention_map(dataset, new_mapname, visual_method, color, bin_size):
        if visual_method == 'attention':
            return Graphs.visual_heatmap(dataset, new_mapname, color, bin_size)
        elif visual_method == 'gaze':
            return Graphs.visual_gaze_plot(dataset, new_mapname)
        else:
            return Graphs.puzzle_image(new_mapname) #If nothing was determined, return a picture of the puzzle

    @staticmethod
    def visual_gaze_plot(dataset, new_mapname):
        '''
        Creates a gazeplot with the associated puzzle map as background

        :author: Yuri Maas
        :param new_mapname: The name of the puzzle to be in the graph
        :param dataset: The Class object from where to take the data
        :return: Graph object with the corresponding map in it
        '''
        imageroute = '/MetroMapsEyeTracking/stimuli/'
        # Load in the associated data (An array of dataframes where every dataframe is 1 user)
        data_puzzle = dataset.get_puzzle_data(new_mapname)
        # Split the data into the x, y, duration, users and custom hover text
        x_coords = [data_puzzle[i]['MappedFixationPointX'] for i in range(len(data_puzzle))]
        y_coords = [data_puzzle[i]['MappedFixationPointY'] for i in range(len(data_puzzle))]
        duration = [data_puzzle[i]['FixationDuration'] for i in range(len(data_puzzle))]
        users = [data_puzzle[i]['user'] for i in range(len(data_puzzle))]
        # Creates the gaze plot graph and returns
        return dcc.Graph(
            id='single-graph',
            config={
                'modeBarButtonsToRemove': [
                    'sendDataToCloud',
                    'zoomIn2d',
                    'zoomOut2d',
                    'hoverClosestCartesian',
                    'hoverCompareCartesian',
                    'autoScale2d',
                    'toggleSpikelines'
                ],
            },
            figure= {
                'data': [go.Scatter(x= x_coords[i],
                                    # The plot has to be horizontally flipped since the y-axis goes from down to up
                                    y= dataset.get_resolution_Y(new_mapname) - y_coords[i],
                                    mode= 'lines+markers',
                                    name= 'User: {}'.format(next(iter(users[i]))),
                                    marker= dict(
                                        # Size of the marker depends on duration
                                        size= np.sqrt(duration[i]),
                                    ),
                                    )
                          for i in range(len(x_coords))],
                'layout': go.Layout(
                    images=[
                        dict(
                            source=imageroute + new_mapname,
                            xref='x',
                            yref='y',
                            x=0,
                            y=0,
                            sizex=dataset.get_resolution_X(new_mapname),
                            sizey=dataset.get_resolution_Y(new_mapname),
                            xanchor='left',
                            yanchor='bottom',
                            opacity=0.8,
                            layer='below',
                            sizing='stretch',
                        )
                    ],
                    title= 'Gaze plot of puzzle: {}'.format(new_mapname[3:-4]),
                    hovermode= 'closest',
                    xaxis=dict(
                        range=[0, dataset.get_resolution_X(new_mapname)],
                        showline= False,
                        showgrid= False,
                        showticklabels= False,
                    ),
                    yaxis=dict(
                        range=[0, dataset.get_resolution_Y(new_mapname)],
                        showline= False,
                        showgrid= False,
                        showticklabels= False,
                    ),
                )
            }
        )

    @staticmethod
    def visual_heatmap(dataset, new_mapname, color, bin_size):
        '''
        Creates a heatmap showing where everyone looked a lot on the map

        :author: Yuri Maas
        :param dataset: The Class object to take the data from
        :param new_mapname: The name of the puzzle that the graph should be based upon
        :param color: Optional color for the heatmap
        :return: Graph object to be visualized by Dash
        '''
        # Load data
        imageroute = '/MetroMapsEyeTracking/stimuli/'
        data_puzzle = dataset.get_puzzle_data(new_mapname)
        # Transform the data into X and Y point separately so they can be used
        x_coords= [data_puzzle[i]['MappedFixationPointX'] for i in range(len(data_puzzle))]
        x_coords= np.concatenate([array for array in x_coords], axis= 0)
        y_coords= [data_puzzle[i]['MappedFixationPointY'] for i in range(len(data_puzzle))]
        y_coords= np.concatenate([array for array in y_coords], axis= 0)
        # Determine the color
        colordict = {
            'def': 'RdBu',
            'hot': 'Hot',
            'green': 'Greens',
            'vir': 'Viridis',
            'elec': 'Electric',
            'rainbow': 'Rainbow',
            'blueish': 'YIGnBu',
        }
        return dcc.Graph(
            id= 'Visual Heatmap',
            figure= {
                'data': [go.Histogram2d(
                    x= x_coords,
                    y= dataset.get_resolution_Y(new_mapname) - y_coords,
                    customdata= new_mapname,
                    zsmooth= 'fast',
                    colorscale= colordict[color],
                    colorbar= dict(
                        showticklabels= False,
                        title= 'Low <--- (Density) ---> High',
                        titleside= 'right',
                    ),
                    xbins= dict(
                        start= 0,
                        end= dataset.get_resolution_X(new_mapname),
                        size= dataset.get_resolution_X(new_mapname)/ bin_size,
                    ),
                    ybins= dict(
                        start= 0,
                        end= dataset.get_resolution_Y(new_mapname),
                        size= dataset.get_resolution_Y(new_mapname)/ bin_size,
                    ),
                    zmax=200,
                    opacity=0.6,
                    )
                ],
                'layout': go.Layout(
                    images=[
                        dict(
                            source=imageroute + new_mapname,
                            xref='x',
                            yref='y',
                            x=0,
                            y=0,
                            sizex=dataset.get_resolution_X(new_mapname),
                            sizey=dataset.get_resolution_Y(new_mapname),
                            xanchor='left',
                            yanchor='bottom',
                            opacity=0.9,
                            layer='below',
                            sizing='stretch',
                        )
                    ],
                    title='Heatmap of puzzle: {}'.format(new_mapname[3:-4]),
                    hovermode='closest',
                    xaxis=dict(
                        range=[0, dataset.get_resolution_X(new_mapname)],
                        showline= False,
                        showgrid= False,
                        showticklabels= True,
                    ),
                    yaxis=dict(
                        range=[0, dataset.get_resolution_Y(new_mapname)],
                        showline= False,
                        showgrid= False,
                        showticklabels= True,
                    ),
                ),
            }
        )