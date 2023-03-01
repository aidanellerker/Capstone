import csv
import pandas as pd
import numpy as np
import gridlabd


def process(parameters):

    
    # Processes data for performance indicator - Overvoltage and Undervoltage
    if parameters[5] == 'Selected' :
        csv_A = pd.read_csv('volts_A1.csv')
        csv_B = pd.read_csv('volts_B1.csv')
        csv_C = pd.read_csv('volts_C1.csv')
    

    # Processes data for performance indicator - Overcurrent and Overloading
    if parameters[6] == 'Selected' :
        print(1)


    # Processes data for performance indicator - Voltage Unbalance Between Phases
    if parameters[7] == 'Selected' :
        print(1)


    # Processes data for performance indicator - Power Losses
    if parameters[8] == 'Selected' :
        print(1)


    # Processes data for performance indicator - Reverse Power Flow in Substation transformers
    if parameters[9] == 'Selected' :
        print(1)

    return