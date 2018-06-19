import pandas as pd
import numpy as np

class Data:
    """
    Class to store the dataset and resolutions in
    This is so the data can't be changed after loading

    :author: Yuri Maas
    """
    def __init__(self, file= "MetroMapsEyeTracking/all_fixation_data_cleaned_up.csv"):
        self.__data, self.__resolutions = self.load_data(file)

    def load_data(self, file):
        """
        Imports the necessary data

        :author: Yuri Maas
        :param file: The file location + name of file of the dataset
        """
        data = pd.read_csv(
            file,
            sep='\t',
            encoding='ISO-8859-1'
        )
        resolutions = pd.read_excel(
            "MetroMapsEyeTracking/stimuli/resolution.xlsx",
            header=None,
            names=['Place', 'x', 'y']
        )[:24]  # Show only the first 24 rows (only rows with resolutions)
        data = self.__preprocess_data(data, resolutions)
        return data, resolutions

    def __preprocess_data(self, data, resolutions):
        """
        Takes the data and prepossesses it

        :author: Yuri Maas
        :param data: The dataset to be preprocessed
        :param resolutions: The resolutions of the maps
        """
        ###### Preprocess functions ####################################
        processed_data = self.__removeFixationsOutsideMap(data, resolutions, 0)
        ################################################################
        return processed_data

    def __removeFixationsOutsideMap(self, data, resolutions, max_pixels):
        """
        Loops over all the fixations and deletes it when the fixation
        point is 'max_pixels' outside the map

        :author: Yuri Maas
        :param data: The dataframe with fixations to be removed
        :param max_pixels: The maximum amount of pixels a fixation is allowed to be outside the map
        """
        for i in range(len(data)):
            # If a stimulus is misspelled, correct it
            text= data.loc[i,('StimuliName')]
            if '04_' in text and '_S2.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='04_Köln_S2.jpg')

            elif '04b_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='04b_Köln_S1.jpg')

            elif '12_' in text and '_S2.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='12_Brüssel_S2.jpg')

            elif '12b_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='12b_Brüssel_S1.jpg')

            elif '14_' in text and '_S2.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='14_Düsseldorf_S2.jpg')

            elif '14b_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='14b_Düsseldorf_S1.jpg')

            elif '15_' in text and '_S2.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='15_Göteborg_S2.jpg')

            elif '15b_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='15b_Göteborg_S1.jpg')

            elif '24_' in text and '_S2.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='24_Zürich_S2.jpg')

            elif '24_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='24_Zürich_S1.jpg')

            elif '24b_' in text and '_S1.jpg' in text:
                data.set_value(index=i, col='StimuliName', value='24b_Zürich_S1.jpg')

            # Gets the mapresolution of the current fixation in the loop
            currentRes = resolutions.get_values()[int(data['StimuliName'][i][:2]) - 1]

            # If a fixation is outside the mapresolution (+- max_pixels), drop the fixation
            if data['MappedFixationPointX'][i] > (currentRes[1] + max_pixels) or (
                    data['MappedFixationPointX'][i] < -max_pixels) or (
                    data['MappedFixationPointY'][i] > (currentRes[2] + max_pixels)) or (
                    data['MappedFixationPointY'][i] < -max_pixels):
                data = data.drop([i])

        # Reset the index of the dataframe index so it goes from 0 to len(data) without skipping
        clean_data = data.reset_index()
        return clean_data
    # End of initialization ################################################################

    def get_data(self):
        """
        Return the dataset

        :author: Yuri Maas
        :return: The entire (processed) dataset
        """
        return self.__data

    def get_puzzle_data(self, puzzle_name):
        '''
        Returns all the fixations of a single puzzle

        :author: Yuri Maas & Annelies vd Wetering
        :param puzzle: The puzzlename to return all the fixations from
        :return: All the fixations of a certain puzzle
        '''
        all_fixations = pd.DataFrame(self.__data.loc[self.__data['StimuliName'] == puzzle_name])
        paths = [pd.DataFrame(all_fixations[all_fixations['user'] == i]) for i in all_fixations['user'].unique()]
        return paths

    def get_resolution_X(self, puzzle_name):
        """
        Return the length of the X-axis (width) of a determined puzzle

        :author: Yuri Maas
        :param puzzle_name: The value name of the puzzle
        :return: width of puzzle
        """
        return self.__resolutions['x'][int(puzzle_name[:2]) - 1]

    def get_resolution_Y(self, puzzle_name):
        """
        Return the length of the Y-axis (height) of a determined puzzle

        :author: Yuri Maas
        :param puzzle_name: The value name of the puzzle
        :return: height of puzzle
        """
        return self.__resolutions['y'][int(puzzle_name[:2]) - 1]

    def get_puzzlenames(self):
        """
        Returns all the names of the puzzles in a dictionary,
         The 'label' has the names without id numbers (The 01 - 24) and .jpg ending,
         The 'value' has the raw names, with id and .jpg

        :author: Yuri Maas
        :return: {'puzzlename_#puzzle', '#map_puzzlename_#puzzle.jpg'}
        """
        return [{'label': i[3:-4], 'value': i} for i in self.__data['StimuliName'].unique()]


class Current_Graphs:
    '''
    A class to store all the current graphs

    :author: Yuri Maas
    '''
    def __init__(self):
        self.__graphs = [None, None, None, None]

    def get_graph(self, graph_id):
        return self.__graphs[graph_id]

    def set_graph(self, graph_id, graph):
        self.__graphs[graph_id] = graph

    def reset_graph(self, graph_id):
        self.__graphs[graph_id] = None