import socket
import time
import numpy as np
import pandas as pd
import serial
import datetime
import os
import yaml
import cardiac.utils.auxiliaryfunctions as aux
import cardiac.communication.periferal as periferal

#%%

correction_dict = dict(first=dict(pre=[], post=[]),
                       last=dict(pre=[], post=[]))

n = 0
HOST = 'DSI-7VPC'
PORT = 6732
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#%%
data = s.recv(1251)

