""" WARNING This code is not ready yet, small functions need to be corrected
 More importantly how is the data going to be store, 
 Python not controlling laser anymore, that is being delegated to the arduino,
 Two Arduinos configuration, 
 First arduino controls receiving the message from Python 
 This arduino sends a pulse to switch the status of the laser
"""

# %%
import socket
import time
from pathlib import Path
import numpy as np
import pandas as pd
import serial
import datetime
from datetime import date
import os
import yaml

import cardiac.communication.serial as cardiac_serial

import cardiac.utils.auxiliaryfunctions as cardiac_aux
import cardiac.utils.metadata as cardiac_metadata
import cardiac.utils.cli as cli

# %%


def compare_laser(laser_in, laser_out):
    if laser_in != laser_out:
        arduino_com.send(laser_out)
        return laser_out
    else:
        return laser_in


def update_laser(id, laserList, status):
    laserList[id] = status
    return laserList


# # %%
# arduino_com = cardiac_serial.ArduinoCommunication()
# arduino_com.start_communication(port='COM4')
# time.sleep(2)
# arduino_com.test_communication()
# %%
# IDLE TIMERS
# experiment_setup = dict(time_1=, time_2=, time=3)
# Here you can set the stim time
idle_timer = cardiac_aux.Timer()
stim_timer = cardiac_aux.Timer()

idle_timer.update([1, 40, 0])
stim_timer.update([2, 0, 0])

clock_zero = datetime.timedelta(hours=0, minutes=0, seconds=0)
# %%
# General Metadata
eMetadata = cardiac_metadata.experimentMetadata(experiment_name='_'.join(['CL-group4_restraint', date.today().strftime("%b-%d-%Y")]),
                                                save=True,
                                                experimenter='CB',
                                                # change folder path here if user is change
                                                experiment_path=r'C:\Users\cbaumerharrison\Documents\CloseLoop',
                                                # FIXME Time recording should start when experiment starts running
                                                # RECORDING TIME [HH, MM, SS]
                                                duration=[5, 30, 0],
                                                day=[6, 0, 0],
                                                night=[19, 0, 0])
# %%
# Idx in python start at 0
# so 0 = 1
# Var pressure loc is found in experiment setup
# number of the first variable [Pressure] is [number-1]
# Window is dependent on acquisition rate
# Example 1m acquisition rate to a window of 6 = 6:00min
print(True)
# %% Subject Metadata
subject_a = cardiac_metadata.subjectMetadata(subjectId='1186971-ChR2',
                                             var_list=['pressure', 'temperature',
                                                       'battery', 'ontime',
                                                       'activity', 'signalst',
                                                       'baro'],
                                             var_pressure_loc=0,
                                             thresholds=dict(day=dict(min=80, max=118),
                                                             night=dict(min=80, max=118)),
                                             parameter='Sys',
                                             laser_trigger='HIGH',
                                             window=6,
                                             laser=dict(stim=True,
                                                        id=0,
                                                        sync=False,
                                                        syncTo=None))

# TODO removing stim duration, create this later to manipulate arduino through python,
# this function is special, think of the possibility of waiting until arduino receives the message
# then build the experiment in the arduino

subject_b = cardiac_metadata.subjectMetadata(subjectId='1195582-ChR2',
                                             var_list=['pressure', 'temperature',
                                                       'battery', 'ontime',
                                                       'activity', 'signalst',
                                                       'baro'],
                                             var_pressure_loc=7,  # change
                                             thresholds=dict(day=dict(min=80, max=116),  # CHANGE THIS LATER
                                                             night=dict(min=80, max=116)),
                                             parameter='Sys',
                                             laser_trigger='HIGH',
                                             window=6,
                                             laser=dict(stim=False,
                                                        id=4,
                                                        sync=False,
                                                        syncTo=None))


subject_c = cardiac_metadata.subjectMetadata(subjectId='1186966-CON',
                                             var_list=['pressure', 'temperature',
                                                       'battery', 'ontime',
                                                       'activity', 'signalst',
                                                       'baro'],
                                             var_pressure_loc=14,
                                             thresholds=dict(day=dict(min=80, max=119),  # CHANGE THIS LATER
                                                             night=dict(min=80, max=119)),
                                             parameter='Sys',
                                             laser_trigger='HIGH',
                                             window=6,
                                             laser=dict(stim=False,
                                                        id=3,
                                                        sync=False,
                                                        syncTo=None))


subject_d = cardiac_metadata.subjectMetadata(subjectId='1186959-ChR2',
                                             var_list=['pressure', 'temperature',
                                                       'battery', 'ontime',
                                                       'activity', 'signalst',
                                                       'baro'],
                                             var_pressure_loc=21,
                                             thresholds=dict(day=dict(min=80, max=120),
                                                             night=dict(min=80, max=120)),
                                             parameter='Sys',
                                             laser_trigger='HIGH',
                                             window=6,
                                             laser=dict(stim=False,
                                                        id=1,
                                                        sync=False,
                                                        syncTo=None))

globalMetadata = cardiac_metadata.mergeMetadataDict(eMetadata,
                                                    cardiac_metadata.mergeSubjectMetadata([subject_a,
                                                                                           subject_b,
                                                                                           subject_c,
                                                                                           subject_d]))

# print(cardiac_metadata.metadataToYaml(globalMetadata))

subject_dict = cli.buildExperiment(globalMetadata['subjects'])
# %%
# if save
# FIXME METADATA DOESN'T SAVE IDLE TIME ETC


def save_path(path, experiment_name):
    path_to_save = Path(os.path.join(path, experiment_name))
    if not path_to_save.exists():
        path_to_save.mkdir(parents=True, exist_ok=True)
        print('Experiment Folder Created\n')
        print(f'Experiment Folder: {path_to_save}')
        return path_to_save
    if path_to_save.exists():
        print('Experiment already created!')
        return path_to_save


def subject_paths(main_path, subject_names):
    for idx in subject_names:
        file_path = main_path.joinpath(idx)
        if not file_path.exists():
            file_path.mkdir(parents=True, exist_ok=True)
            print(f'Subject Folder: {file_path}')
    print('Experiment Folder Created\n')


if globalMetadata['save']:

    path_to_save = save_path(globalMetadata['experiment_path'],
                             globalMetadata['experiment_name'])
    subject_paths(path_to_save, subject_dict.keys())

    cardiac_metadata.metadataToYaml(globalMetadata, path_to_save)

    for subject_idx in subject_dict.keys():
        for indv_data in subject_dict[subject_idx].data:
            subject_dict[subject_idx].data[indv_data].create_csv(
                path_to_save, subject_idx)


# %% Communications -------------------------------------
dsi_com = cardiac_serial.DSICommunications()
dsi_com.start_communications()

# %%
# # Arduino must be plugged in by now
# This code connectes to the arduino to send the signal dependent on Var [Ex. Sys]
# COM4 referes to the USB port in which the arduino is connected, the name is not tide to the location
# Go to the right corner to get the name
# COM4 in this case is attached to Arduino Nano Every
# if you press serial monitor light should blink
# make sure that baud rate is set at 9600
# If you open serial monitor remember to close it pressing the "X"

arduino_com = cardiac_serial.ArduinoCommunication()
arduino_com.start_communication(port='COM4')
# time.sleep(5)
# arduino_com.test_communication()
# dsi_com.test_communication()
# %%
search_list = list()
for name in subject_dict.keys():
    search_list.extend(subject_dict[name].datamap)

# %%  START RECORDING

experiment_time = cli.startExperiment(globalMetadata)
idle_timer.startTimer()
idle_timer.get_remainingtime()
idle_Clock = True
stim_Clock = True
stimState = False
laserState = [0, 0, 0, 0]
laserCurrent = [0, 0, 0, 0]
BP_Status = []
i = 0  # Fix later
print('Experiment: <-----Started----->')
while experiment_time.remaining_time > clock_zero:
    new_data = dsi_com.recv_data()
    if new_data:
        recv_data = new_data.decode().split(',')
    # NOTE too complex code better...
    # Maybe get laser controls out of the dataframe
        val_recv = list(
            filter(lambda x: recv_data[0].__contains__(x[1]), search_list))

        if val_recv:
            val_recv = val_recv[0]
            subject_dict[val_recv[0]].data[val_recv[1]].update_df(recv_data)

            # CLOCKS
            # IDLE TIMER

            if stimState:

                if subject_dict[val_recv[0]].laser['stim']:
                    # extract parameter to test against
                    test_val = subject_dict[val_recv[0]].data[val_recv[1]].moving_average(
                        subject_dict[val_recv[0]].threshold.window,
                        subject_dict[val_recv[0]].threshold.parameter)

                    if test_val:
                        recv_laser = subject_dict[val_recv[0]].threshold.get_laser_state(
                            test_val, experiment_time.get_current_time())
                        if not subject_dict[val_recv[0]].laser['sync']:
                            laserState = update_laser(subject_dict[val_recv[0]].laser['id'], laserState,
                                                      int(recv_laser[1]))

                            arduino_com.send(
                                subject_dict[val_recv[0]].laser['id'], int(recv_laser[1]))

                            subject_dict[val_recv[0]].data['laser'].update_df(
                                recv_laser)
                        elif subject_dict['test_subject'].laser['sync']:
                            # TODO Fix function later
                            print('to be continue...')
                        if globalMetadata['save']:
                            subject_dict[val_recv[0]].data['laser'].save_data(
                                path_to_save, val_recv[0])

            if globalMetadata['save']:
                subject_dict[val_recv[0]].data[val_recv[1]
                                               ].save_data(path_to_save, val_recv[0])

    # print idle clock if available
    # TODO Fix this timer idle + Stim

    if idle_timer.timeRemaining <= clock_zero:
        idle_Clock = False
        if stim_Clock:
            stim_timer.startTimer()
            stim_timer.get_remainingtime()

        if stim_timer.timeRemaining > clock_zero:
            stimState = True
            stim_Clock = False

        elif stim_timer.timeRemaining <= clock_zero:
            if i <= 3:
                arduino_com.send(i, 0)
                laserState = update_laser(i, laserState, 0)
            stimState = False
            i += 1

    if idle_Clock:
        idle_timer.get_remainingtime()
        # print(f'idle time remaining: {idle_timer.timeRemaining}')

    if stimState:
        stim_timer.get_remainingtime()
        # print(f'Stim time remaining: {stim_timer.timeRemaining}')
    # this send the laser state to the arduino if it changes
    # laserCurrent = compare_laser(laserCurrent, laserState)
    experiment_time.get_remainingtime()
    print(
        f'Laser State: {laserState} time remaining: {experiment_time.remaining_time}', end='\r')
print('Experiment: <-----Ended----->')
time.sleep(5)
for i in range(4):
    if i <= 3:
        arduino_com.send(i, 0)
        time.sleep(1)
print('Experiment: <-----Lasers OFF----->')
print('Experiment: <-----DONE----->')
# %%

# %%
