import gridlabd

global parameters

def modify_glm(params):
    parameters = params
    # TODO make this a variable
    gridlabd.command('R1_12_47_3.glm')
    gridlabd.start('wait')
    print(gridlabd.get_value('R1-12-47-3_ol_27', 'length'))

def on_init(t):
    gridlabd.set_value('R1-12-47-3_ol_27', 'length', '208.69')
    return True