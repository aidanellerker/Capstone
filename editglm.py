import gridlabd

def modify_glm(params):

    

    # TODO make this a variable
    gridlabd.command('R1_12_47_3.glm')

    print(gridlabd.get_global('starttime'))
    gridlabd.start('wait')