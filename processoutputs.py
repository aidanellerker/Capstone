import csv
import pandas as pd
import numpy as np
import gridlabd


def process(parameters):
    # Window size for moving averages
    window_tenmins = round(600 / int(parameters[2]))
    window_onehour = round(3600 / int(parameters[2]))
    window_twohours = round(7200 / int(parameters[2]))

    # ANSI C84.1 range violations
    # Service voltage, >600 V
    rangeA_upper = 1.05
    rangeA_lower = 0.975
    rangeB_upper = 1.058
    rangeB_lower = 0.95


    # Processes data for performance indicator - Overvoltage and Undervoltage
    if parameters[5] == 'Selected' :

        # Deletes header info from CSVs
        with open('volts_A.csv', 'r') as f:
            lines = f.readlines()
        with open('volts_A.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('volts_B.csv', 'r') as f:
            lines = f.readlines()
        with open('volts_B.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('volts_C.csv', 'r') as f:
            lines = f.readlines()
        with open('volts_C.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])
            

        # converts CSVs to numpy 2D arrays
        A = open("volts_A.csv")
        A_array = np.genfromtxt(A, delimiter=",", dtype='str')

        B = open("volts_B.csv")
        B_array = np.genfromtxt(B, delimiter=",", dtype='str')

        C = open("volts_C.csv")
        C_array = np.genfromtxt(C, delimiter=",", dtype='str')


        # slicing arrays
        nodes = A_array[0, 1:]
        times = A_array[1:, 0]
        A1_vals = np.abs(A_array[1:, 1:].astype(complex))
        B1_vals = np.abs(B_array[1:, 1:].astype(complex))
        C1_vals = np.abs(C_array[1:, 1:].astype(complex))


        ### initialized arrays for processed info
        max_VA = np.empty((2, len(nodes)), dtype='object') # first row, timestamp of max/min for each node 
        min_VA = np.empty((2, len(nodes)), dtype='object') # second row, value of max/min for each node
        movingavg_VA = np.zeros((len(times)-(window_tenmins-1), len(nodes)))
        max_VB = np.empty((2, len(nodes)), dtype='object')
        min_VB = np.empty((2, len(nodes)), dtype='object')
        movingavg_VB = np.zeros((len(times)-(window_tenmins-1), len(nodes)))
        max_VC = np.empty((2, len(nodes)), dtype='object')
        min_VC = np.empty((2, len(nodes)), dtype='object')
        movingavg_VC = np.zeros((len(times)-(window_tenmins-1), len(nodes)))
        # Also violation_A, violation_B, violation_C instantiated below
        ###


        # put data in per unit
        for idx, name in enumerate(nodes):
            item = gridlabd.get_value(name, "nominal_voltage")
            Vbase = float(item[:-2])
            A1_vals[:,idx] = A1_vals[:,idx]/Vbase
            B1_vals[:,idx] = B1_vals[:,idx]/Vbase
            C1_vals[:,idx] = C1_vals[:,idx]/Vbase

        
        # determine maxs and mins for each node at each phase
        max_VA[0] = [times[T] for T in np.argmax(A1_vals, axis=0)]
        max_VA[1] = np.amax(A1_vals, axis=0)

        min_VA[0] = [times[T] for T in np.argmin(A1_vals, axis=0)]
        min_VA[1] = np.amin(A1_vals, axis=0)

        max_VB[0] = [times[T] for T in np.argmax(B1_vals, axis=0)]
        max_VB[1] = np.amax(B1_vals, axis=0)

        min_VB[0] = [times[T] for T in np.argmin(B1_vals, axis=0)]
        min_VB[1] = np.amin(B1_vals, axis=0)

        max_VC[0] = [times[T] for T in np.argmax(C1_vals, axis=0)]
        max_VC[1] = np.amax(C1_vals, axis=0)

        min_VC[0] = [times[T] for T in np.argmin(C1_vals, axis=0)]
        min_VC[1] = np.amin(C1_vals, axis=0)


        # calculating moving average
        tmp = np.ones(window_tenmins)/window_tenmins
        for i in range(len(nodes)):
            movingavg_VA[:, i] = np.convolve(A1_vals[:, i], tmp, mode='valid')
            movingavg_VB[:, i] = np.convolve(B1_vals[:, i], tmp, mode='valid')
            movingavg_VC[:, i] = np.convolve(C1_vals[:, i], tmp, mode='valid')


        # array of violations
        violation_A =  movingavg_VA.copy()
        for (x,y), value in np.ndenumerate(violation_A):
            if value >= rangeB_upper:
                violation_A[x,y] = 2
            elif value >= rangeA_upper:
                violation_A[x,y] = 1
            elif value <= rangeB_lower:
                violation_A[x,y] = -2
            elif value <= rangeA_lower:
                violation_A[x,y] = -1
            else:
                violation_A[x,y] = 0

        violation_B = movingavg_VB.copy()
        for (x,y), value in np.ndenumerate(violation_B):
            if value >= rangeB_upper:
                violation_B[x,y] = 2
            elif value >= rangeA_upper:
                violation_B[x,y] = 1
            elif value <= rangeB_lower:
                violation_B[x,y] = -2
            elif value <= rangeA_lower:
                violation_B[x,y] = -1
            else:
                violation_B[x,y] = 0

        violation_C = movingavg_VC.copy()
        for (x,y), value in np.ndenumerate(violation_C):
            if value >= rangeB_upper:
                violation_C[x,y] = 2
            elif value >= rangeA_upper:
                violation_C[x,y] = 1
            elif value <= rangeB_lower:
                violation_C[x,y] = -2
            elif value <= rangeA_lower:
                violation_C[x,y] = -1
            else:
                violation_C[x,y] = 0


    # Processes data for performance indicator - Overcurrent and Overloading
    if parameters[6] == 'Selected' :
        # Deletes header info from CSVs
        with open('line_currentA.csv', 'r') as f:
            lines = f.readlines()
        with open('line_currentA.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('line_currentB.csv', 'r') as f:
            lines = f.readlines()
        with open('line_currentB.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('line_currentC.csv', 'r') as f:
            lines = f.readlines()
        with open('line_currentC.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])


        # converts CSVs to numpy 2D arrays
        A_current = open("line_currentA.csv")
        A_array_current = np.genfromtxt(A_current, delimiter=",", dtype='str')

        B_current = open("line_currentB.csv")
        B_array_current = np.genfromtxt(B_current, delimiter=",", dtype='str')

        C_current = open("line_currentC.csv")
        C_array_current = np.genfromtxt(C_current, delimiter=",", dtype='str')
   
    
        # slicing arrays
        nodes_current = A_array_current[0, 1:]
        times_current = A_array_current[1:, 0]
        A1_vals_current = np.abs(A_array_current[1:, 1:].astype(complex))
        B1_vals_current = np.abs(B_array_current[1:, 1:].astype(complex))
        C1_vals_current = np.abs(C_array_current[1:, 1:].astype(complex))


        ### initialized arrays for processed info (current in lines)
        max_IA = np.empty((2, len(nodes_current)), dtype='object') # first row, timestamp of max for each line 
        movingavg_IA = np.zeros((len(times_current)-(window_onehour-1), len(nodes_current)))
        max_IB = np.empty((2, len(nodes_current)), dtype='object')
        movingavg_IB = np.zeros((len(times_current)-(window_onehour-1), len(nodes_current)))
        max_IC = np.empty((2, len(nodes_current)), dtype='object')
        movingavg_IC = np.zeros((len(times_current)-(window_onehour-1), len(nodes_current)))
        # Also violation_A, violation_B, violation_C instantiated below
        ###


        # put data in per unit
        for idx, name in enumerate(nodes_current):
            item_current = gridlabd.get_value(name, "continuous_rating")  
            Ibase = float(item_current[:-2])
            A1_vals_current[:,idx] = A1_vals_current[:,idx]/Ibase
            B1_vals_current[:,idx] = B1_vals_current[:,idx]/Ibase
            C1_vals_current[:,idx] = C1_vals_current[:,idx]/Ibase


        # determine maxs for each line at each phase
        max_IA[0] = [times_current[T] for T in np.argmax(A1_vals_current, axis=0)]
        max_IA[1] = np.amax(A1_vals_current, axis=0)

        max_IB[0] = [times_current[T] for T in np.argmax(B1_vals_current, axis=0)]
        max_IB[1] = np.amax(B1_vals_current, axis=0)

        max_IC[0] = [times_current[T] for T in np.argmax(C1_vals_current, axis=0)]
        max_IC[1] = np.amax(C1_vals_current, axis=0)


        # calculating moving average
        tmp_current = np.ones(window_onehour)/window_onehour
        for i in range(len(nodes_current)):
            movingavg_IA[:, i] = np.convolve(A1_vals_current[:, i], tmp_current, mode='valid')
            movingavg_IB[:, i] = np.convolve(B1_vals_current[:, i], tmp_current, mode='valid')
            movingavg_IC[:, i] = np.convolve(C1_vals_current[:, i], tmp_current, mode='valid')


        max_current = 1.00
        # array of violations
        violation_A_current =  movingavg_IA.copy()
        for (x,y), value in np.ndenumerate(violation_A_current):
            if value > max_current:
                violation_A_current[x,y] = 1
            else:
                violation_A_current[x,y] = 0

        violation_B_current =  movingavg_IB.copy()
        for (x,y), value in np.ndenumerate(violation_B_current):
            if value > max_current:
                violation_B_current[x,y] = 1
            else:
                violation_B_current[x,y] = 0

        violation_C_current =  movingavg_IC.copy()
        for (x,y), value in np.ndenumerate(violation_C_current):
            if value > max_current:
                violation_C_current[x,y] = 1
            else:
                violation_C_current[x,y] = 0
        



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