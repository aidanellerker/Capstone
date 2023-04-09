import userparameters
import editglm
import processoutputs
import gridlabd

# this displays the data form and stores all the parameters as a list
params = userparameters.data_form()

# this edits the glm file AND runs the simulation
editglm.modify_glm(params)

# this processes the output CSV files
processoutputs.process(params)

# this visualizes the resulting data
processoutputs.visualize(params)