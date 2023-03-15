import gridlabd

def modify_glm(params):
    global parameters
    parameters = params
    #loads glm file and runs
    gridlabd.command(params[0])
    gridlabd.start('wait')


def on_init(t):

    #sets climate tmy file
    climate = find("class=climate")
    gridlabd.set_value(climate[0], 'tmyfile', parameters[1])

    #sets timestep by adjusting interval for all necessary objects
    recorder = find("class=metrics_collector")
    for object in recorder:
        gridlabd.set_value(object, 'interval', parameters[2])

    recorder = find("class=metrics_collector_writer")
    for object in recorder:
        gridlabd.set_value(object, 'interval', parameters[2])

    recorder = find("class=group_recorder")
    for object in recorder:
        gridlabd.set_value(object, 'interval', parameters[2])

    #sets start and stop time
    gridlabd.set_global('clock', parameters[3])
    gridlabd.set_global('starttime', parameters[3])
    gridlabd.set_global('stoptime', parameters[4])

    #sets battery efficiencies
    batteries = find("class=battery")
    for object in batteries:
        gridlabd.set_value(object, 'round_trip_efficiency', parameters[17])

    #sets inverter efficiencies
    inverters = find("class=inverter")
    for object in inverters:
        gridlabd.set_value(object, 'inverter_efficiency', parameters[18])

    #sets PV efficiencies
    PVpanels = find("class=solar")
    for object in PVpanels:
        gridlabd.set_value(object, 'efficiency', parameters[19])

    #sets EV charger types
    EVchargers = find("class=evcharger")
    for object in EVchargers:
        gridlabd.set_value(object, 'charger_type', parameters[20])
    
    #sets inverter pfs
    for object in inverters:
        gridlabd.set_value(object, 'power_factor', parameters[21])

    #sets hysteresis curve values
    bat_inverters = []
    for name in batteries :
        item = gridlabd.get_object(name)
        bat_inverters.append(item["parent"])
    for object in bat_inverters:
        gridlabd.set_value(object, 'charge_on_threshold', parameters[22]+" kW")
        gridlabd.set_value(object, 'charge_off_threshold', parameters[23]+" kW")
        gridlabd.set_value(object, 'discharge_off_threshold', parameters[24]+" kW")
        gridlabd.set_value(object, 'discharge_on_threshold', parameters[25]+" kW")
        gridlabd.set_value(object, 'max_charge_rate', parameters[26]+" kW")
        gridlabd.set_value(object, 'max_discharge_rate', parameters[27]+" kW")
    
    #sets if large-scale PV and/or battery are active at feeder
    PV_inverters = []
    for name in PVpanels :
        item = gridlabd.get_object(name)
        PV_inverters.append(item["parent"])

    if parameters[13] == "None" :
        gridlabd.set_value(bat_inverters[len(bat_inverters)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(PV_inverters[len(PV_inverters)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(batteries[len(batteries)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(PVpanels[len(PVpanels)-1], 'generator_status', 'OFFLINE')
    elif parameters[13] == "PV-Cells" :
        gridlabd.set_value(bat_inverters[len(bat_inverters)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(PV_inverters[len(PV_inverters)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(batteries[len(batteries)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(PVpanels[len(PVpanels)-1], 'generator_status', 'ONLINE')
    elif parameters[13] == "Battery Storage" :
        gridlabd.set_value(bat_inverters[len(bat_inverters)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(PV_inverters[len(PV_inverters)-1], 'generator_status', 'OFFLINE')
        gridlabd.set_value(batteries[len(batteries)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(PVpanels[len(PVpanels)-1], 'generator_status', 'OFFLINE')
    elif parameters[13] == "Both" :
        gridlabd.set_value(bat_inverters[len(bat_inverters)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(PV_inverters[len(PV_inverters)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(batteries[len(batteries)-1], 'generator_status', 'ONLINE')
        gridlabd.set_value(PVpanels[len(PVpanels)-1], 'generator_status', 'ONLINE')

    #sets large-scale PV installation area
    gridlabd.set_value(PVpanels[len(PVpanels)-1], 'area', parameters[14]+' ft^2')

    #sets large-scale battery installation capacity
    gridlabd.set_value(batteries[len(batteries)-1], 'battery_capacity', parameters[15]+' kWh')

    #sets large-scale installation inverter rated power
    gridlabd.set_value(bat_inverters[len(bat_inverters)-1], 'rated_power', parameters[16]+" kVA")
    gridlabd.set_value(PV_inverters[len(PV_inverters)-1], 'rated_power', parameters[16]+" kVA")

    #sets penetration levels for PV, battery, EV charger
    PV_proportion = round(float(parameters[10]) * (len(PVpanels)-1)) #excludes last one, which is large-scale installation
    bat_proportion = round(float(parameters[11]) * (len(batteries)-1))
    EV_proportion = round(float(parameters[12]) * len(EVchargers))

    #
    for x in range(PV_proportion) :
        gridlabd.set_value(PVpanels[x], 'generator_status', 'ONLINE')
        gridlabd.set_value(PV_inverters[x], 'generator_status', 'ONLINE')
    for y in range(PV_proportion, len(PVpanels)-1) :
        gridlabd.set_value(PVpanels[y], 'generator_status', 'OFFLINE')
        gridlabd.set_value(PV_inverters[y], 'generator_status', 'OFFLINE')
    #
    for x in range(bat_proportion) :
        gridlabd.set_value(batteries[x], 'generator_status', 'ONLINE')
        gridlabd.set_value(bat_inverters[x], 'generator_status', 'ONLINE')
    for y in range(bat_proportion, len(batteries)-1) :
        gridlabd.set_value(batteries[y], 'generator_status', 'OFFLINE')
        gridlabd.set_value(bat_inverters[y], 'generator_status', 'OFFLINE')
    #
    for x in range(EV_proportion, len(EVchargers)) :
        gridlabd.set_value(EVchargers[x], 'state', 'WORK')
        gridlabd.set_value(EVchargers[x], 'p_go_home', '0.00000')
    

    return True



def find(criteria) :
    finder = criteria.split("=")
    if len(finder) < 2 :
        raise Exception("find(criteria='key=value'): criteria syntax error")
    objects = gridlabd.get("objects")
    result = []
    for name in objects :
        item = gridlabd.get_object(name)
        if finder[0] in item and item[finder[0]] == finder[1] :
            if "name" in item.keys() :
                result.append(item["name"])
            else :
                result.append("%s:%s" % (item["class"],item["id"]))
    return result