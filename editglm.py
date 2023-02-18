import gridlabd

def modify_glm(params):
    global parameters
    parameters = params
    # TODO make this a variable
    gridlabd.command('R1_12_47_3.glm')
    gridlabd.start('wait')


def on_init(t):
    #sets timestep by adjusting interval for all recorders
    

    #sets start and stop time
    gridlabd.set_global('clock', parameters[1])
    gridlabd.set_global('starttime', parameters[1])
    gridlabd.set_global('stoptime', parameters[2])

    return True