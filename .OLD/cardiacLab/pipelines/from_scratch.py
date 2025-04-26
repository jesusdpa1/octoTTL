import socket
import time
import numpy as np
import pandas as pd
import serial
import datetime
import os
import yaml
#%%
# subject_list = {'1038132-CON': {'pressure_var_location': 0,
#                                 'stim': True,
#                                 'stim_duration': {'hour': 1, 'min': 00, 'sec': 00}, 'stim_wait': 10},
#                 '1038133-ChR2': {'pressure_var_location': 4,
#                                  'stim': True,
#                                  'stim_duration': {'hour': 1, 'min': 00, 'sec': 00}, 'stim_wait': 10},
#                 '1038134-CON': {'pressure_var_location': 8,
#                                 'stim': True,
#                                 'stim_duration': {'hour': 1, 'min': 00, 'sec': 00}, 'stim_wait': 10},
#                 '1038135-ChR2': {'pressure_var_location': 12,
#                                  'stim': True,
#                                  'stim_duration': {'hour': 1, 'min': 00, 'sec': 00}, 'stim_wait': 10},
#                 '1038181-ChR2': {'pressure_var_location': 16,
#                                  'stim': True,
#                                  'stim_duration': {'hour': 1, 'min': 00, 'sec': 00}, 'stim_wait': 10},
#                 }


#%%
def create_metadata():
    dict(experiment_id='',
         date='',
         )

def load_experiment():
    print('experiment loaded')

class ExperimentMetadata:
    def __init__(self, experiment_id, user_name, time_day, time_night, subj_list,
                 rec_time=dict(hour=0, min=0, sec=0), path_to_save=os.getcwd()):

        self.experiment_id = experiment_id
        self.user_name = user_name
        self.start_time = datetime.datetime.now().ctime()
        self.end_time = (self.start_time +
                         datetime.timedelta(hours=rec_time['hour'], min=rec_time['min'], sec=rec_time['sec'])).ctime()
        self.recording_time = rec_time
        self.rec_DayTime = time_day
        self.rec_NightTime = time_night
        self.SubjectList = subj_list
        self.ExperimentDirectory = path_to_save


class SetThreshold:
    def __init__(self, var_name, parameter, day_min, day_max, night_min, night_max):
        self.var_name = var_name
        self.parameter = parameter
        self.day_min = day_min
        self.day_max = day_max
        self.night_min = night_min
        self.night_max = night_max


class SubjectMetadata:
    def __init__(self, var_list, var_pressure_loc, stim, stim_duration, stim_wait, threshold, stim_type, subj_stim_sync=None):
        self.var_list = var_list
        self.var_pressure_loc = var_pressure_loc
        self.stim = stim
        self.stim_duration = stim_duration
        self.stim_wait = stim_wait
        self.threshold = threshold
        self.stim_type = stim_type
        self.subj_stim_sync = subj_stim_sync

    def get_var_df(self, var_name):
        if var_name == 'pressure':
            return DSIVars().df_pressure
        if var_name == 'temperature':
            return DSIVars().df_temperature
        if var_name == 'signalst':
            return DSIVars().df_signalst
        if var_name == 'baro':
            return DSIVars().df_baro
        if var_name == 'ontime':
            return DSIVars().df_ontime
        if var_name == 'laser':
            return DSIVars().df_laser
        if var_name == 'activity':
            return DSIVars().df_activity
        if var_name == 'battery':
            return DSIVars().df_battery

    def get_org_dict(self):
        orgdict = dict()
        org_length = list(np.arange(self.var_pressure_loc,
                          self.var_pressure_loc + len(self.var_list)).astype('str'))

        pre_res = [''.join([';', sub]) for sub in org_length]
        suf_res = [''.join([sub, ';0']) for sub in pre_res]
        i = 0
        for var_name in self.var_list:
            orgdict[suf_res[i]] = dict(id=var_name, df=self.get_var_df(var_name))
            i = i + 1
        return orgdict


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
        self.df_activity = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'A_Num', 'A_Mean', 'A_RMax', 'A_RMin',
                                                 'A_Per', 'A_BPM', 'A_Area', 'A_TA', 'A_NPMN', 'A_TA2', 'A_Coun', 'A_CT',
                                                 'A_Samp'])

        # SIGNAL ST
        self.df_signalst = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'Num', 'Mean', 'RMax', 'RMin', 'Period',
                                                 'BPM', 'Area', 'TA', 'NPMN', 'TA2', 'Count', 'CT', 'SampSD'])

        # BARO / APR
        self.df_baro = pd.DataFrame(columns=['ElapsedTime', 'RealTime', 'Event', 'B_Num', 'B_Mean', 'B_RMax', 'B_RMin', 'B_Per',
                                             'B_BPM', 'B_Area', 'B_TA', 'B_NPMN', 'B_TA2', 'B_Coun', 'B_CT', 'B_Samp'])

        # LASER
        self.df_laser = pd.DataFrame(columns=['ElapsedTime', 'laser', 'day_cycle', 'night_cycle', 'min_threshold',
                                              'max_threshold'])


#%%


def get_pin_map(sub_list):
    arduino_dict = dict()
    i = 2
    for key_subject in sub_list.keys():
        arduino_dict[key_subject] = {'pin': str(i), 'stim': subject_list[key_subject]['stim']}
        i = i + 1
    return arduino_dict


#%%
subject_list = dict()

subject_list["1038132-CON"] = SubjectMetadata(var_list=['pressure', 'activity', 'signalst', 'baro'],
                                              var_pressure_loc=0,
                                              stim=True,
                                              stim_duration={"hour": 1, "min": 00, "sec": 00},
                                              stim_wait={"hour": 0, "min": 10, "sec": 00},
                                              threshold=SetThreshold(var_name="pressure",
                                                                      parameter="Sys",
                                                                      day_min=10,
                                                                      day_max=80,
                                                                      night_min=10,
                                                                      night_max=80),
                                              stim_type="sync",
                                              subj_stim_sync="1038132-CON")

subject_list["1038133-ChR2"] = SubjectMetadata(var_list=['pressure', 'activity', 'signalst', 'baro'],
                                               var_pressure_loc=0,
                                               stim=False,
                                               stim_duration={"hour": 1, "min": 00, "sec": 00},
                                               stim_wait={"hour": 0, "min": 10, "sec": 00},
                                               threshold=SetThreshold(var_name="pressure",
                                                                      parameter="Sys",
                                                                      day_min=10,
                                                                      day_max=80,
                                                                      night_min=10,
                                                                      night_max=80),
                                               stim_type="sync",
                                               subj_stim_sync="1038132-CON")

#%%
subject_list['1038132-CON'].get_org_dict()
#%%

n = 0
HOST = 'DSI-7VPC'
PORT = 6732
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#%%


def start_loop(sec):
    for n in range(sec):
        data = s.recv(1251)
        if data:
            print(f"program starts in {sec-n}")
            data = []
        time.sleep(1)


#%%


#%%
start_loop(10)
while True:
    # if (final_time - datetime.datetime.now()) > 0: ##????
    n = n + 1
    data = s.recv(1251)  # 1251 * buffer size has to be increase by the number of subjects - 1
    data_recv = data.decode('cp1252').split('\x00')
    if data_recv:
        for data_line in data_recv:
            print(data_line.split(','))
        data_recv = []


    

