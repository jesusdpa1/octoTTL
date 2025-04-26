import os
import time
import numpy as np
import pandas as pd
import serial
import socket
import datetime
import functools
import operator

import yaml


# EXPERIMENT DEPENDANT OBJECTS

# TODO fix time functions, maybe create its own class or python functions under auxiliary functions since two classes are using them

# TIME FUNCTIONS ----------------------------------------------------------

class Timer:
    def __init__(self) -> None:
        self.timeDuration = None
        self.timeStart = None
        self.timeEnd = None
        self.timeRemaining = None

    def update(self, timeDuration: list):
        """[summary]

        Args:
            timeDuration (list): time in the format of [hour, min, sec]

        Returns:
            [type]: [description]
        """
        self.timeDuration = self.timeToDateTime(timeDuration)

    def resetTimer(self):
        self.timeStart = None
        self.timeEnd = None
        self.timeRemaining = None

    def startTimer(self):
        self.timeStart = datetime.datetime.now()
        self.calc_endtime()

    # Function regarding time

    def calc_endtime(self):
        self.timeEnd = self.math_time(
            [self.timeStart, self.get_timedelta(self.timeDuration)], 'add')

    def get_remainingtime(self, verbose=False):
        self.timeRemaining = self.math_time(
            [self.timeEnd, datetime.datetime.now()], 'sub')
        if verbose:
            print(f'time Remaining: {self.timeRemaining.__str__()}', end='\r')

    def printVals(self):
        print(f'time duration: {self.timeDuration.__str__()}')
        print(f'start time: {self.timeStart.__str__()}')
        print(f'end time: {self.timeEnd.__str__()}')

    @staticmethod
    def timeToDateTime(time_list):
        """
        :param time_list: [hour, minutes, seconds]
        :return:
        """
        if time_list is None:
            print('no value introduce, setting time to 0h:0m:0s')
            time_list = [0, 0, 0]
        if not isinstance(time_list, list):
            print(
                'input values should be a list of len 3 [hour, minute, second]')
        if isinstance(time_list, list):
            return datetime.time(hour=time_list[0], minute=time_list[1], second=time_list[2])

    @staticmethod
    def get_timedelta(time_conversion):
        return datetime.timedelta(hours=time_conversion.hour,
                                  minutes=time_conversion.minute,
                                  seconds=time_conversion.second)

    @staticmethod
    def math_time(time_list, math_fun):
        if isinstance(time_list, list):
            if math_fun == 'add':
                return functools.reduce(operator.add, time_list)
            if math_fun == 'sub':
                return functools.reduce(operator.sub, time_list)
        if not isinstance(time_list, list):
            print('values not in list structure')


class DateTime:

    def __init__(self):
        self.recording_time = datetime.time(hour=0, minute=0, second=0)
        self.remaining_time = datetime.time(hour=0, minute=0, second=0)
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.day = datetime.time(hour=0, minute=0, second=0)
        self.night = datetime.time(hour=0, minute=0, second=0)
        self.current_time = None

    def update_datetime(self,
                        time_list=None,
                        cycle=None):
        if cycle is None:
            print('cycle missing')

        if cycle:
            if cycle == 'day':
                self.day = self.update_time(time_list)
            if cycle == 'night':
                self.night = self.update_time(time_list)

    def update_rectime(self, time_list=None):

        self.recording_time = self.update_time(time_list)
        self.end_time = self.math_time(
            [self.start_time, self.get_timedelta(self.recording_time)], 'add')
        print(f'Experiment will end at {self.end_time.__str__()}')

    def get_remainingtime(self, verbose=False):
        self.remaining_time = self.math_time(
            [self.end_time, datetime.datetime.now()], 'sub')
        if verbose:
            print(self.remaining_time)

    def get_current_time(self):
        if (datetime.datetime.now().time() >= self.day) & (datetime.datetime.now().time() <= self.night):
            self.current_time = 'day'
            return 'day'

        if not (datetime.datetime.now().time() >= self.day) & (datetime.datetime.now().time() <= self.night):
            self.current_time = 'night'
            return 'night'

    @staticmethod
    def get_timedelta(time_conversion):
        return datetime.timedelta(hours=time_conversion.hour,
                                  minutes=time_conversion.minute,
                                  seconds=time_conversion.second)

    @staticmethod
    def math_time(time_list, math_fun):
        if isinstance(time_list, list):
            if math_fun == 'add':
                return functools.reduce(operator.add, time_list)
            if math_fun == 'sub':
                return functools.reduce(operator.sub, time_list)
        if not isinstance(time_list, list):
            print('values not in list structure')

    @staticmethod
    def update_time(time_list):
        """
        :param time_list: [hour, minutes, seconds]
        :return:
        """
        if time_list is None:
            print('no value introduce, setting time to 0h:0m:0s')
            time_list = [0, 0, 0]
        if not isinstance(time_list, list):
            print(
                'input values should be a list of len 3 [hour, minute, second]')
        if isinstance(time_list, list):
            return datetime.time(hour=time_list[0], minute=time_list[1], second=time_list[2])

    def print_intervals(self):
        print(f'recording time: {self.recording_time.__str__()}')
        print(f'start time: {self.start_time.__str__()}')
        print(f'end time: {self.end_time.__str__()}')
        print(f'day cycle start: {self.day.__str__()}')
        print(f'night cycle start: {self.night.__str__()}')
        print(f'current cycle: {self.get_current_time()}')


class ThresholdLimits:
    # TODO Fix how Threshold is build
    def __init__(self):
        self.time = dict(day=dict(min=0, max=0), night=dict(min=0, max=0))
        self.parameter = None
        self.laser_state = False
        self.laser_trigger = None
        self.window = None
        self.counterUp = 0
        self.counterDown = 0
        self.timerFlag = False

    def update_threshold(self, threshold_val=None, parameter=None, laser_trigger=None, window=None):

        # Threshold
        if isinstance(threshold_val, dict):
            self.time = threshold_val

        elif not isinstance(threshold_val, dict):
            print(
                'input values should be a dict(day=dict(min=0, max=0), night=dict(min=0, max=0))')

        # Parameter
        if isinstance(parameter, str):
            self.parameter = parameter
        elif not isinstance(parameter, str):
            print('input values for parameter should be a string like "Sys"')

        # laser_trigger
        if isinstance(laser_trigger, str):
            self.laser_trigger = laser_trigger
        elif not isinstance(laser_trigger, str):
            print('input values for parameter should be a string like "HIGH"')

        # Window length
        if isinstance(window, int):
            self.window = window
        elif not isinstance(window, int):
            print('input values for parameter should be an int')

        # stim_duration

    # Get the laser state, this will trigger the laser
    def get_laser_state(self, var_value, time_cycle) -> list:
        state = None
        if var_value >= self.time[time_cycle]['min'] and var_value <= self.time[time_cycle]['max']:
            state = 'NORMAL'
        elif var_value < self.time[time_cycle]['min']:
            state = 'LOW'
            # print(f'WARNING {self.parameter} value {state}: {var_value}')
        elif var_value > self.time[time_cycle]['max']:
            state = 'HIGH'
            # print(f'WARNING {self.parameter} value {state}: {var_value}')
        # apply function depending on time remaining of the stim
        # TODO REVIEW THIS

        if self.laser_trigger == state:
            self.counterUp = self.counterUp + 1
            self.counterDown = 0
            self.counter()
        elif 'NORMAL' == state:
            self.counterDown = self.counterDown + 1
            self.counterUp = 0
            self.counter()
        elif 'LOW' == state:
            self.counterDown = self.counterDown + self.window + 10  # REVIEW this 10 later
            self.counterUp = 0
            self.laser_state = False
            # FIXME add message that explains that the variable is the reason
            # print(f'WARNING Turning LASER OFF')

        return [datetime.datetime.now().ctime(),
                self.laser_state,
                time_cycle,
                state,
                var_value]

    def turnOFF(self, time_cycle,):  # FIXME Add 10 seconds of shutting down the system
        self.laser_state = False
        state = 'Turning-OFF'
        var_value = None
        return [datetime.datetime.now().ctime(),
                self.laser_state,
                time_cycle,
                state,
                var_value]

    def counter(self):
        # COUNTER
        if self.counterUp > self.window:
            self.laser_state = True
            self.counterDown = 0
            # print(
            #     f'WARNING {self.parameter} Turning LASER ON\n time remaining ')

        if self.counterDown > self.window:
            self.laser_state = False
            self.counterUp = 0


# %% SUBJECT DEPENDANT OBJECTS


class DSIVars:
    def __init__(self):
        self.df_pressure = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'Num', 'Sys', 'Dia',
                                                 'Mean', 'PH', 'HR', 'TTPK', 'ET', 'neg_dP/dt', 'pos_dP/dt', 'REC',
                                                 'NPMN', 'Q-A', 'RNum', 'RInt', 'RBpm', 'Mean2', 'PTTs', 'PWVs',
                                                 'PTTed', 'PWVed', 'IBIs', 'IBIms', 'IBIed', 'Count'])

        # TEMPERATURE
        self.df_temperature = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'T_Num', 'T_Mean',
                                                    'T_RMax', 'T_RMin', 'T_Per', 'T_BPM', 'T_Area', 'T_TA',
                                                    'T_NPMN', 'T_TA2', 'T_Coun', 'T_CT', 'T_Samp'])

        # BATTERY
        self.df_battery = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'Num', 'Mean', 'RMax', 'RMin',
                                                'Period', 'BPM', 'Area', 'TA', 'NPMN', 'TA2', 'Count', 'CT', 'SampSD'])

        # OnTime
        self.df_ontime = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'Num', 'Mean', 'RMax', 'RMin',
                                               'Period', 'BPM', 'Area', 'TA', 'NPMN', 'TA2', 'Count', 'CT', 'SampSD'])

        # ACTIVITY
        self.df_activity = pd.DataFrame(
            columns=['ElapsedTime', 'RealTime', 'Event', 'A_Num', 'A_Mean', 'A_RMax', 'A_RMin',
                     'A_Per', 'A_BPM', 'A_Area', 'A_TA', 'A_NPMN', 'A_TA2', 'A_Coun', 'A_CT',
                     'A_Samp'])

        # SIGNAL ST
        self.df_signalst = pd.DataFrame(
            columns=['ElapsedTime', 'RealTime', 'Event', 'Num', 'Mean', 'RMax', 'RMin', 'Period',
                     'BPM', 'Area', 'TA', 'NPMN', 'TA2', 'Count', 'CT', 'SampSD'])

        # BARO / APR
        self.df_baro = pd.DataFrame(
            columns=['ElapsedTime', 'RealTime', 'Event', 'B_Num', 'B_Mean', 'B_RMax', 'B_RMin', 'B_Per',
                     'B_BPM', 'B_Area', 'B_TA', 'B_NPMN', 'B_TA2', 'B_Coun', 'B_CT', 'B_Samp'])

        # LASER
        self.df_laser = pd.DataFrame(
            columns=['ElapsedTime', 'laser', 'time_cycle', 'state', 'parameter_value'])

    def get_var_df(self, var_name):
        if var_name == 'pressure':
            return self.df_pressure
        if var_name == 'temperature':
            return self.df_temperature
        if var_name == 'signalst':
            return self.df_signalst
        if var_name == 'baro':
            return self.df_baro
        if var_name == 'ontime':
            return self.df_ontime
        if var_name == 'laser':
            return self.df_laser
        if var_name == 'activity':
            return self.df_activity
        if var_name == 'battery':
            return self.df_battery
        if var_name == 'laser':
            return self.df_laser

# FIXME correct DataDict, to complicated, should be a search function not dependant on the acquisition of the data


class DataDict:
    """[summary]
    """

    def __init__(self, id, location, df):
        """[summary]

        Args:
            id ([type]): variable_name
            df ([type]): dataframe from DSIVars
            location (int): index location of receiving data
        """
        self.id = id
        self.location = location
        self.csv_name = ''.join([self.id, '.csv'])
        self.df = df

    def len(self):
        print(len(self.df))

    def update_df(self, datao):
        data_len = len(self.df)
        self.df.loc[data_len, :] = datao
        self.df.loc[data_len, :] = self.df.loc[data_len,
                                               :].replace(r'', 0, regex=True)

    def create_csv(self, main_path, subject):
        file_name = main_path.joinpath(subject, self.csv_name)
        if file_name.exists():
            print(f'file already exists {file_name.is_file()}')
        if not file_name.exists():
            self.df.to_csv(file_name, header=True)
            print(f'file created: {subject}: {self.csv_name}')

    def save_data(self, main_path, subject):
        file_name = main_path.joinpath(subject, self.csv_name)
        self.df.tail(1).to_csv(file_name, mode='a', header=False)

    # Function to extract relevant data from the desire parameter
    def check_parameter(self, parameter):
        if parameter in self.df.keys():
            return True
        else:
            return False

    def last_val(self, parameter):
        # extract the last value of the specific parameter in the df
        if self.check_parameter(parameter):
            return float(self.df.loc[self.df.index[-1], parameter])
        elif not self.check_parameter(parameter):
            return None

    def moving_median(self, win_len, parameter):
        if self.check_parameter(parameter):
            if len(self.df) > win_len:
                index_last = self.df.index[-1]
                index_first = index_last - win_len
                return self.df.loc[index_first:index_last, parameter].astype('float64').median()
            if len(self.df) < win_len:
                return None
        elif not self.check_parameter(parameter):
            return None

    def moving_average(self, win_len, parameter):
        if self.check_parameter(parameter):
            if len(self.df) > win_len:
                index_last = self.df.index[-1]
                index_first = index_last - win_len
                return self.df.loc[index_first:index_last, parameter].astype('float64').mean()
            if len(self.df) < win_len:
                return None
        elif not self.check_parameter(parameter):
            return None

    def moving_max(self, win_len, parameter):
        if self.check_parameter(parameter):
            if len(self.df) > win_len:
                index_last = self.df.index[-1]
                index_first = index_last - win_len
                return self.df.loc[index_first:index_last, parameter].astype('float64').max()
            if len(self.df) < win_len:
                return None
        elif not self.check_parameter(parameter):
            return None

    def moving_min(self, win_len, parameter):
        if self.check_parameter(parameter):
            if len(self.df) > win_len:
                index_last = self.df.index[-1]
                index_first = index_last - win_len
                return self.df.loc[index_first:index_last, parameter].astype('float64').min()
            if len(self.df) < win_len:
                return None
        elif not self.check_parameter(parameter):
            return None
# %%


def get_data_dict(var_list, var_list_loc):
    """[summary]

    Args:
        var_pressure_loc (int): [description]
        var_list (list): [description]

    Returns:
        [dict]: dictionary containing  the case dataset
    """
    # remember not to add laser to the var list

    dsi_vars = DSIVars()
    data_df = list(map(lambda x: dsi_vars.get_var_df(x), var_list))
    # Use the DataDict function to store the data
    data_list = list(zip(var_list,
                         var_list_loc,
                         data_df))

    data_list = list(map(lambda x: DataDict(
        id=x[0], location=x[1], df=x[2]), data_list))

    return dict(zip(var_list_loc, data_list))

# %% correct arduino dict

# %%
# if save == true
# create a table with all the vars pressure where row one is the location in the transmitted data
#
# create hdf5 dict
# load the last 10, moving window
