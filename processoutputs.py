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
        # Overcurrent
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
        # Also violation_A_current, violation_B_current, violation_C_current instantiated below
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


        # Overloading
        # Deletes header info from CSV
        with open('R1_12_47_3_transformer_power_in.csv', 'r') as f:
            lines = f.readlines()
        with open('R1_12_47_3_transformer_power_in.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])


        # converts CSV to numpy 2D array
        power_in = open("R1_12_47_3_transformer_power_in.csv")
        power_in_array = np.genfromtxt(power_in, delimiter=",", dtype='str')


        # slicing array
        nodes_power = power_in_array[0, 1:]
        times_power = power_in_array[1:, 0]
        power_in_vals = np.abs(power_in_array[1:, 1:].astype(complex))


        ### initialized array for processed info (power in transformers)
        max_P = np.empty((2, len(nodes_power)), dtype='object') # first row, timestamp of max for each line 
        movingavg_P= np.zeros((len(times_power)-(window_twohours-1), len(nodes_power)))


        # put data in per unit
        for idx, name in enumerate(nodes_power):
            item_power = gridlabd.get_value(name, "continuous_rating")  
            Sbase = float(item_power[:-2])*1000              # Multiply by 1000, because S ratings are in kVA
            power_in_vals[:,idx] = power_in_vals[:,idx]/Sbase


        # determine maxs for each transformer 
        max_P[0] = [times_power[T] for T in np.argmax(power_in_vals, axis=0)]
        max_P[1] = np.amax(power_in_vals, axis=0)


        # calculating moving average
        tmp_power = np.ones(window_twohours)/window_twohours
        for i in range(len(nodes_power)):
            movingavg_P[:, i] = np.convolve(power_in_vals[:, i], tmp_power, mode='valid')


        max_power = 1.20
        # array of violations
        violation_power =  movingavg_P.copy()
        for (x,y), value in np.ndenumerate(violation_power):
            if value > max_power:
                violation_power[x,y] = 1
            else:
                violation_power[x,y] = 0


        # Processes data for performance indicator - Voltage Unbalance Between Phases
    if parameters[7] == 'Selected' :
        if parameters[5] == 'Not Selected':
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
        else:
            # converts CSVs to numpy 2D arrays
            AU = open("volts_A.csv")
            AU_array = np.genfromtxt(AU, delimiter=",", dtype='str')

            BU = open("volts_B.csv")
            BU_array = np.genfromtxt(BU, delimiter=",", dtype='str')

            CU = open("volts_C.csv")
            CU_array = np.genfromtxt(CU, delimiter=",", dtype='str')

            # slicing arrays

            nodes = AU_array[0, 1:]
            times = AU_array[1:, 0]
            A1U_vals = np.abs(AU_array[1:, 1:].astype(complex))
            B1U_vals = np.abs(BU_array[1:, 1:].astype(complex))
            C1U_vals = np.abs(CU_array[1:, 1:].astype(complex))



            #initalize the parameters
            movingavg_VAU = np.zeros((len(times)-(window_tenmins-1), len(nodes)))
            movingavg_VBU = np.zeros((len(times)-(window_tenmins-1), len(nodes)))
            movingavg_VCU = np.zeros((len(times)-(window_tenmins-1), len(nodes)))

            tmp = np.ones(window_tenmins)/window_tenmins
            for i in range(len(nodes)):
                movingavg_VAU[:, i] = np.convolve(A1U_vals[:, i], tmp, mode='valid')
                movingavg_VBU[:, i] = np.convolve(B1U_vals[:, i], tmp, mode='valid')
                movingavg_VCU[:, i] = np.convolve(C1U_vals[:, i], tmp, mode='valid')

            #using a lot of the following code from Miyu's voltage unbalance calculator
            nodesA = list(movingavg_VAU)[1:]
            nodesA_dict = dict.fromkeys(nodesA,0)
            voltage_unbalances = dict.fromkeys(tuple(nodes),times)

            for node in movingavg_VAU:
                for index in movingavg_VAU:
                    phase_A = complex(movingavg_VAU[node][index].replace('i','j')) 
            nested = []
            nested_node = []

            matA = np.array([1,1,1,1, (-0.5-0.866j), (-0.5+0.866j), 1, (-0.5+0.866j), (-0.5-0.866j)]).reshape(3,3) #matrix used for the Fortescue transformation
            matA_inv = np.linalg.inv(matA) #inverse 

            violationPU = np.empty_like(movingavg_VAU)
            phase_voltages = [movingavg_VAU, movingavg_VBU, movingavg_VCU]
            nested_node.append(phase_voltages)
            nested.append(phase_voltages)
            
            #test = voltages

            for node in nested:
                for phase_voltages in node:
                    np.array(phase_voltages)
                    Vs = np.matmul(matA_inv, node) 

            for i in Vs[1:i] :
                Vs_fail = abs(Vs[2].item()/Vs[1].item())
                for (x,y), value in np.ndenumerate(Vs_fail):
                    if Vs_fail(x,y) > 0.2 : 
                        violationPU =np.copy(Vs_fail(x,y))
                
                





            #nested list of phase voltages
            
            #nested_node.append(phase_voltages)
            #nested.append(nested_node)

            #node_index = 0
            #time_index = 0
            #violationP = []
            #the calculator for phase violation, not too sure how it works but I know the matrix multiplication is from the transform
            #for node in nested:
                #for voltages in node:
                    #voltages = np.array(voltages)
                    #Vs =np.matmul(matA_inv, voltages.reshape(3,1))
                    #if abs(Vs[2].item()/Vs[1].item()) > 0.02:
                        #violationP = np.insert(Vs)
                        


              #not sure which values to take for the moving avgs
              # calculating moving average
            #tmp = np.ones(window_tenmins)/window_tenmins
            #for i in range(len(nodes)):
                #movingavg_VA[:, i] = np.convolve(A1_vals[:, i], tmp, mode='valid')
                #movingavg_VB[:, i] = np.convolve(B1_vals[:, i], tmp, mode='valid')
                #movingavg_VC[:, i] = np.convolve(C1_vals[:, i], tmp, mode='valid')


    # Processes data for performance indicator - Power Losses
    if parameters[8] == 'Selected' :
        
        # Deletes header info from CSVs
        with open('losses_overhead_line.csv', 'r') as f:
            lines = f.readlines()
        with open('losses_overhead_line.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('losses_underground_line.csv', 'r') as f:
            lines = f.readlines()
        with open('losses_underground_line.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])

        with open('losses_transformer.csv', 'r') as f:
            lines = f.readlines()
        with open('losses_transformer.csv', 'w') as f:
            f.write(lines[8][1:]+'\n')
            f.writelines(lines[9:])


        # converts CSVs to numpy 2D arrays
        losses_overhead = open("losses_overhead_line.csv")
        losses_overhead_array = np.genfromtxt(losses_overhead, delimiter=",", dtype='str')

        losses_underground = open("losses_underground_line.csv")
        losses_underground_array = np.genfromtxt(losses_underground, delimiter=",", dtype='str')

        losses_transformer = open("losses_transformer.csv")
        losses_transformer_array = np.genfromtxt(losses_transformer, delimiter=",", dtype='str')


        # slicing arrays
        losses_overhead_vals = np.abs(losses_overhead_array[1:, 1:].astype(complex))
        losses_underground_vals = np.abs(losses_underground_array[1:, 1:].astype(complex))
        losses_transformer_vals = np.abs(losses_transformer_array[1:, 1:].astype(complex))



    # Processes data for performance indicator - Reverse Power Flow in Substation transformers
    if parameters[9] == 'Selected' :
        if parameters[6] == 'Not Selected':
            with open('R1_12_47_3_transformer_power_in.csv', 'r') as f:
                lines = f.readlines()
            with open('R1_12_47_3_transformer_power_in.csv', 'w') as f:
                f.write(lines[8][1:]+'\n')
                f.writelines(lines[9:])
        else:
            power_inR = open("R1_12_47_3_transformer_power_in.csv")
            power_inR_array = np.genfromtxt(power_inR, delimiter=",", dtype='str')
            
            
        # slicing arrays

        power_inR_vals = np.sign(np.real(power_inR_array[1:, 1:].astype(complex)))
        
        # counting how many times there is reverse power flow in transformers
        violation_PR = np.zeros_like(power_inR_vals)

        for (x,y), value in np.ndenumerate(power_inR_vals):
            if power_inR_vals[x,y] == -1:
                violation_PR[x,y] == 1
            else:
                violation_PR[x,y] == 0 
      

        #calculate total time
        Rtimes = np.sum(violation_PR)
        Rtotal = Rtimes/violation_PR.size         #total times/size of array should give a fraction, multiply Atotal by the total run time
        timeR = Rtotal * int(parameters[2])

    
    return