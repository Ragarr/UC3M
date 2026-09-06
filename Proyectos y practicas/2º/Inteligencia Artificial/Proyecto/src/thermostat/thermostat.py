import pandas as pd
from .state import State
from .action import Action
from .markov_model import MDP


class Thermostat(MDP):
    """
    Class that represents the thermostat problem
    """
    def __init__(self, path_data_on:str, path_data_off: str, objetive_temp: str,
                cost_on: str, cost_off: str):
        """
        Constructor of the class
        :param path_data_on: Path to the .csv file with the data of the ON action
        :param path_data_off: Path to the .csv file with the data of the OFF action
        :param inital_temp: Initial temperature of the thermostat
        :param objetive_temp: Temperature that the thermostat must reach
        :param cost_on: Cost of the ON action
        :param cost_off: Cost of the OFF action
        """
        self.cost_on = cost_on
        self.cost_off = cost_off
        self.objective = objetive_temp
        self.data_ON = self.__dataframe_creation(path_data_on)
        self.data_OFF = self.__dataframe_creation(path_data_off)

        states_df = self.data_ON.columns.values.tolist() # get states from dataframe
        self.states = [] # List of states of type(State)
        # create actions list for each state
        i = 0
        for state in states_df:
            probabilities_ON = dict(self.data_ON.iloc[i])
            action_on = Action("Turn ON", self.cost_on, probabilities_ON, str(state))
            probabilities_OFF = dict(self.data_OFF.iloc[i])
            action_off = Action("Turn OFF", self.cost_off, probabilities_OFF, str(state))
            actions = [action_on, action_off]
            self.states.append(State(str(state), actions))
            i += 1

        self._update_V()

    def __str__(self):
        text = ""
        for state in self.states:
            text += "V(" + str(state.id) + "): " + str(round(state.V, 3)) + "\n"
            text += "Acción recomendada: " + str(state.prefered_action) + "\n"
        return text

    def __dataframe_creation(self, file) -> pd.DataFrame:
        """
        Creates a dataframe from .csv
        :param file: .csv directory
        :return:
        """
        data_frame = pd.read_csv(file, index_col=0, sep=',')
        data_frame.fillna(0, inplace=True)
        return data_frame

