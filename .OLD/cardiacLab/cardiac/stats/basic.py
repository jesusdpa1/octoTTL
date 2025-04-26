import socket
import time
import numpy as np
import pandas as pd
import serial
import datetime
import os
import yaml

# REVIEW....
class ExtractValue:
    def __init__(self, df):
        self.df