import socket
import time
import numpy as np
import pandas as pd
import serial
import datetime
import os
import yaml

import cardiac.communication.serial as cardiac_serial
import cardiac.utils.auxiliaryfunctions as cardiac_aux


#%%
subject_metadata = dict()
# any variable location will be the number in Ponehma minus 1 (-1)
subject_metadata["1038132-CON"] = cardiac_aux.SubjectMetadata(var_list=['pressure', 'activity', 'signalst', 'baro'],
                                              var_pressure_loc=183,

                                              stim_duration={"hour": 1, "min": 00, "sec": 00},
                                              stim_wait={"hour": 0, "min": 10, "sec": 00},

                                              threshold=cardiac_aux.SetThreshold(var_name="pressure",
                                                                                 parameter="Sys",
                                                                                 tresh_vals=dict(
                                                                                     day=dict(min=80, max=100),
                                                                                     night=dict(min=80, max=100)),
                                                                                 moving_window=False,
                                                                                 time_day=dict(hour=5, min=0, sec=0),
                                                                                 time_night=dict(hour=18, min=0, sec=0),
                                                                                 rec_time=dict(hour=24, min=0, sec=0)
                                                                                 ),
                                              stim=True,
                                              stim_type="sync",
                                              subj_stim_sync="1038132-CON")

subject_metadata["1038133-ChR2"] = cardiac_aux.SubjectMetadata(var_list=['pressure', 'activity', 'signalst', 'baro'],
                                               var_pressure_loc=187,
                                               stim_duration={"hour": 1, "min": 00, "sec": 00},
                                               stim_wait={"hour": 0, "min": 10, "sec": 00},
                                               threshold=cardiac_aux.SetThreshold(var_name="pressure",
                                                                                  parameter="Sys",
                                                                                  tresh_vals=dict(
                                                                                      day=dict(min=80, max=100),
                                                                                      night=dict(min=80, max=100)),
                                                                                  moving_window=False,
                                                                                  time_day=dict(hour=5, min=0, sec=0),
                                                                                  time_night=dict(hour=18, min=0, sec=0),
                                                                                  rec_time=dict(hour=24, min=0, sec=0),
                                                                                  ),
                                               stim=False,
                                               stim_type="sync",
                                               subj_stim_sync="1038132-CON")

#%%
# dictionary to store the data
subject_dict = dict()
for key_name in subject_metadata.keys():
    subject_dict[key_name] = subject_metadata[key_name].get_org_dict()


#%%
"""
Start connection with serial terminal (DSI)
HOST and PORT information gotten from the DSI Ponemah software

"""
n = 0
HOST = 'DSI-7VPC'
PORT = 6732
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#%%
"""
main loop to acquire and process the data
"""

cardiac_serial.start_loop(s, 5)
data_struct = cardiac_serial.RecvData()
while True:
    # if (final_time - datetime.datetime.now()) > 0: ##????
    data = s.recv(1251)
    data_recv = data.decode('cp1252').split('\x00')
    if data_recv[0] == '':
        data_recv.pop(0)
    data_struct.update(recv_data=data_recv)
    if data_recv:
        data_analysis = cardiac_serial.DataEntry(data_struct.clean_data())
        for datao in data_analysis.data:
            for key_subject in subject_dict.keys():
                for key_var in subject_dict[key_subject].keys():
                    if datao.__contains__(key_var):
                        subject_dict[key_subject][key_var].update_df(datao.split(','))
                        # data_len = len(subject_dict[key_subject][key_var]['df'])
                        # subject_dict[key_subject][key_var]['df'].loc[data_len, :] = datao.split(',')
                        if subject_metadata[key_subject].threshold.var_name[0] == subject_dict[key_subject][key_var].id: #['id']:
                            parameter = subject_metadata[key_subject].threshold.parameter[0]
                            var_value = subject_dict[key_subject][key_var].lastval(parameter=parameter)
                            laser_state = subject_metadata[key_subject].threshold.get_laser_state(key_subject, var_value)
                            subject_dict[key_subject]['laser'].update_df(laser_state)

        data_recv = []

#%%
win_len = 4
index_last = subject_dict[key_subject][key_var].df.index[-1]
index_first = index_last - win_len
float(subject_dict[key_subject][key_var].df.loc[index_first:index_last, parameter].median())

#%%
class ArduinoCommunication:
    def __init__(self):
        self.map = None
        self.stim_time = None
    def arduino_map(self, subject_list, arduino_pin):
        arduino_dict = dict()
        for i, key_subject in enumerate(subject_list):
            arduino_dict[key_subject] = {'pin': str(i+arduino_pin)}
        self.map = arduino_dict

    def send_signal(self, arduino_serial, key_subject):
        arduino_serial.write(str.encode(''.join([self.map[key_subject]['pin'], '-OFF;'])))
        # write here to reset clock

#%%
arduino_dict = cardiac_aux.ArduinoCommunication()
arduino_dict.arduino_map(list(subject_metadata.keys()), 4)
#%%