import tkinter
from tkinter import W, ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def data_form():
    window = tkinter.Tk()  #main window
    window.title("Input Parameters for Simulation")

    def enter_data():
        tlength = time_spinbox.get()
        starttime = start_entry.get()
        stoptime = stop_entry.get()
        p1 = pi1_var.get()
        p2 = pi2_var.get()
        p3 = pi3_var.get()
        p4 = pi4_var.get()
        p5 = pi5_var.get()
        PV_pen = res_PV_spinbox.get()
        bat_pen = res_bat_spinbox.get()
        EV_pen = res_EV_spinbox.get()
        install = lc_install_box.get()
        peff = PV_eff_spinbox.get()
        Parea = PV_entrybox.get()
        ev = EV_charger_box.get()
        beff = bat_eff_box.get()
        bcap = bat_cap_box.get()
        ieff = inv_eff_box.get()
        ipow = inv_pow_box.get()
        ipf = inv_pf_box.get()

        chargeOnThreshold = charge_on_threshold_box.get()
        chargeOffThreshold = charge_off_threshold_box.get()
        dischargeOffThreshold = discharge_off_threshold_box.get()
        dischargeOnThreshold = discharge_on_threshold_box.get()
        maxChargeRate = max_charge_rate_box.get()
        maxDischargeRate = max_discharge_rate_box.get()

        
        print("Chosen .glm file:", glm_file, "Chosen .tmy2 file: ", tmy_file)
        print("Time-step Length:", tlength, "Start Time:", starttime, "Stop Time:", stoptime)
        print("Chosen Perfomance Indices:", p1,p2,p3,p4,p5)
        print("Residential PV Penetration:", PV_pen, "Residential Battery Storage Penetration:", bat_pen, "Residential EV Charger Penetration:", EV_pen)
        print("Large Scale Installation:", install, "PV Area:", Parea, "Battery Capacity:", bcap)
        print("Inverter Rated Power:", ipow, "Battery Efficiency:", beff, "Inverter Efficiency:", ieff)
        print("PV efficiency:", peff, "EV Charger Type:", ev, "Inverter Power Factor:", ipf)
        print("Charge On Threshold:", chargeOnThreshold, "Charge Off Threshold:", chargeOffThreshold, "Discharge Off Threshold:", dischargeOffThreshold)
        print("Discharge On Threshold:", dischargeOnThreshold, "Max Charge Rate:", maxChargeRate, "Max Discharge Rate:", maxDischargeRate)
        print("------------------------------------------------------")
        
        #closes window so that program can continue
        window.quit()

        global param_list

        param_list = [glm_file, tmy_file, tlength, starttime, stoptime, p1, p2, p3, p4, p5,
        PV_pen, bat_pen, EV_pen, install, Parea, bcap, ipow, beff, ieff, peff,
        ev, ipf, chargeOnThreshold, chargeOffThreshold, dischargeOffThreshold, dischargeOnThreshold, maxChargeRate, maxDischargeRate]

    




    frame = tkinter.Frame(window)
    frame.pack()  

    #main frame section 1
    main_frame1 = tkinter.LabelFrame(frame, text="Please select the corresponding file types (NECESSARY)")       #first param is parent
    main_frame1.grid(row= 0, column=0, padx=20, pady=10, sticky="news")
    for widget in main_frame1.winfo_children():
        widget.grid_configure(padx=10, pady=5)
    #glm file reader
    glm_title = tkinter.Label(main_frame1, text = "Please select a .glm file")
    glm_title.grid(row=0,column=0,pady=10)
    def select_file():
        glmfiletypes = (
            ('glm files', '*.glm'),
            ('All files', '*.*')
        )
        global glm_file
        glm_file = fd.askopenfilename(title ='Open a file (.glm file)', initialdir='/',filetypes=glmfiletypes)
        showinfo(title="Selected File", message=glm_file)
    openglm = ttk.Button(main_frame1, text='Choose a file', command=select_file)
    openglm.grid(row=0, column=1, sticky ='news',pady=10)

    #tmy file reader
    tmy_title = tkinter.Label(main_frame1, text = "Please select a .tmy2 file")
    tmy_title.grid(row=1,column=0, pady=10)
    def select_file2():
        tmyfiletypes = (
            ('tmy2 files', '*.tmy2'),
            ('tmy3 files', '*.tmy3'),
            ('All files', '*.*')
        )
        global tmy_file
        tmy_file = fd.askopenfilename(title ='Open a file (.tmy2 file)', initialdir='/',filetypes=tmyfiletypes)
        showinfo(title="Selected File", message=tmy_file)
    opentmy = ttk.Button(main_frame1, text='Choose a file', command=select_file2)
    opentmy.grid(row=1, column=1, sticky ='news',pady=10)

    #main frame section 2
    main_frame2 = tkinter.LabelFrame(frame, text = "Select the following parameters for the simulation to run")
    main_frame2.grid (row= 1, column=0, padx = 20, pady = 10, sticky="news")

    for widget in main_frame2.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    time_step = tkinter.Label(main_frame2, text = "Time-step Length in seconds [60,600]")
    time_spinbox = tkinter.Spinbox(main_frame2, from_=60, to =600, increment=5)
    time_step.grid(row=0,column =0)
    time_spinbox.grid(row=1,column =0)

    start_time = tkinter.Label(main_frame2, text = "Choose a start time")
    start_var = tkinter.StringVar(main_frame2)
    start_var.set("2000-01-01 00:00:00")
    start_entry = tkinter.Entry(main_frame2, textvariable=start_var)
    start_time.grid(row=0,column=1)
    start_entry.grid(row=1, column =1)

    stop_time = tkinter.Label(main_frame2, text="Choose a stop time [yyyy-mm-dd hr:mm:ss]")
    stop_var = tkinter.StringVar(main_frame2)
    stop_var.set("2000-01-01 01:00:00")
    stop_entry = tkinter.Entry(main_frame2, textvariable=stop_var)
    stop_time.grid(row=0,column=2)
    stop_entry.grid(row=1, column=2)


    #main frame section 3
    main_frame3 = tkinter.LabelFrame(frame, text = "Select any/all performance indicators you would like to assess (pick at least 1)")
    main_frame3.grid(row = 2, column=0, padx = 20, pady = 10, sticky="news")
    for widget in main_frame3.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    pi1_var = tkinter.StringVar(value= "Not selected")
    performance1_check = tkinter.Checkbutton(main_frame3,text = "ANSI Voltage Standard", variable = pi1_var, onvalue="Selected" , offvalue="Not Selected")
    performance1_check.grid(sticky = W, row=0,column=1)

    pi2_var = tkinter.StringVar(value= "Not selected")
    performance2_check = tkinter.Checkbutton(main_frame3,text = "Overcurrent and Overloading", variable = pi2_var, onvalue="Selected" , offvalue="Not Selected")
    performance2_check.grid(sticky = W, row=1,column=1)

    pi3_var = tkinter.StringVar(value= "Not selected")
    performance3_check = tkinter.Checkbutton(main_frame3,text = "Voltage Unbalance", variable = pi3_var, onvalue="Selected" , offvalue="Not Selected")
    performance3_check.grid(sticky = W, row=2,column=1)

    pi4_var = tkinter.StringVar(value= "Not selected")
    performance4_check = tkinter.Checkbutton(main_frame3,text = "Losses in Line", variable = pi4_var, onvalue="Selected" , offvalue="Not Selected")
    performance4_check.grid(sticky = W, row=3,column=1)

    pi5_var = tkinter.StringVar(value= "Not selected")
    performance5_check = tkinter.Checkbutton(main_frame3,text = "Power Flow in Substation Transformers", variable = pi5_var, onvalue="Selected" , offvalue="Not Selected")
    performance5_check.grid(sticky = W, row=4,column=1)


    #main frame section 4
    main_frame4 = tkinter.LabelFrame(frame, text = "Select a value for the following parameters (Area, Capacity, and Rated Power are large-scale installation values)")
    main_frame4.grid(row = 3, column=0, padx = 20, pady = 10, sticky="news")
    for widget in main_frame4.winfo_children():
        widget.grid_configure(padx=10, pady=5)


    res_PV_pen = tkinter.Label(main_frame4, text = 'Residential PV Penetration [0,1]')
    res_PV_spinbox = tkinter.Spinbox(main_frame4, from_=0, to_=1, increment=0.05)
    res_PV_pen.grid(row=0, column=0)
    res_PV_spinbox.grid(row=1, column=0)

    res_bat_pen = tkinter.Label(main_frame4, text = 'Residential Battery Storage Penetration [0,1]')
    res_bat_spinbox = tkinter.Spinbox(main_frame4, from_=0, to_=1, increment=0.05)
    res_bat_pen.grid(row=0, column=1)
    res_bat_spinbox.grid(row=1, column=1)

    res_EV_pen = tkinter.Label(main_frame4, text = 'Residential EV Charger Penetration [0,1]')
    res_EV_spinbox = tkinter.Spinbox(main_frame4, from_=0, to_=1, increment=0.05)
    res_EV_pen.grid(row=0, column=2)
    res_EV_spinbox.grid(row=1, column=2)

    lc_install = tkinter.Label(main_frame4, text="Large-Scale Installation")
    lc_install_box = ttk.Combobox(main_frame4, values = ["None", "PV-Cells", "Battery Storage", "Both"])
    lc_install_box.current(0)
    lc_install.grid(row =4, column=0)
    lc_install_box.grid(row=5, column=0)

    PV_area = tkinter.Label(main_frame4, text = "PV Area [in sq.ft]")
    PV_area_var=tkinter.StringVar(main_frame4)
    PV_area_var.set("2500")
    PV_entrybox = tkinter.Entry(main_frame4, textvariable=PV_area_var)
    PV_area.grid(row=4, column=1)
    PV_entrybox.grid(row = 5, column=1)

    bat_cap = tkinter.Label(main_frame4, text = "Battery Capacity [in kWh]")
    bat_cap_var=tkinter.StringVar(main_frame4)
    bat_cap_var.set("1000")
    bat_cap_box = tkinter.Entry(main_frame4, textvariable=bat_cap_var)
    bat_cap.grid(row=4, column=2)
    bat_cap_box.grid(row = 5, column=2)

    inv_pow= tkinter.Label(main_frame4, text = "Per-Phase Inverter Rated Power [in kVA]")
    inv_pow_var=tkinter.StringVar(main_frame4)
    inv_pow_var.set("100")
    inv_pow_box=ttk.Spinbox(main_frame4, from_=0, to_=200000, increment=1000, textvariable=inv_pow_var)
    inv_pow.grid(row= 4, column =3)
    inv_pow_box.grid(row=5, column=3)

    #main frame section 5
    main_frame5 = tkinter.LabelFrame(frame, text = "Select a value for the following parameters")
    main_frame5.grid(row = 4, column=0, padx = 20, pady = 10, sticky="news")
    for widget in main_frame5.winfo_children():
        widget.grid_configure(padx=10, pady=5)


    bat_eff = tkinter.Label(main_frame5, text= "Battery Efficiency [0,1]")
    bat_eff_var = tkinter.StringVar(main_frame5)
    bat_eff_var.set("0.90")
    bat_eff_box = ttk.Spinbox(main_frame5, from_=0, to_=1, increment=0.01, textvariable=bat_eff_var)
    bat_eff.grid(row=0,column=0)
    bat_eff_box.grid(row=1, column =0)

    PV_eff = tkinter.Label(main_frame5, text = 'PV Efficiency [0,1]')
    PV_eff_var = tkinter.StringVar(main_frame5)
    PV_eff_var.set("0.15")
    PV_eff_spinbox = tkinter.Spinbox(main_frame5, from_=0, to_=1, increment=0.01, textvariable=PV_eff_var)
    PV_eff.grid(row=0, column=2)
    PV_eff_spinbox.grid(row=1, column=2)

    EV_charger = tkinter.Label(main_frame5, text= "EV Charger Type")
    EV_charger_box = ttk.Combobox(main_frame5, values=["LOW","MEDIUM","HIGH"])
    EV_charger_box.current(0)
    EV_charger.grid(row=4,column = 0)
    EV_charger_box.grid(row=5, column =0)

    inv_eff=tkinter.Label(main_frame5, text="Inverter Efficiency [0,1]")
    inv_eff_var=tkinter.StringVar(main_frame5)
    inv_eff_var.set("0.90")
    inv_eff_box=ttk.Spinbox(main_frame5, from_=0, to_=1, increment=0.01, textvariable=inv_eff_var)
    inv_eff.grid(row=0, column=1)
    inv_eff_box.grid(row=1, column=1)

    inv_pf=tkinter.Label(main_frame5, text="Inverter Power Factor [0,1]") 
    inv_pf_var=tkinter.StringVar(main_frame5)
    inv_pf_var.set("1.00")
    inv_pf_box=ttk.Spinbox(main_frame5, from_=0, to_=1, increment=0.01, textvariable=inv_pf_var)
    inv_pf.grid(row =4, column=1)
    inv_pf_box.grid(row=5, column =1)

    #main frame section 6
    main_frame6 = tkinter.LabelFrame(frame, text = "Battery hysteresis curve parameters")
    main_frame6.grid (row= 5, column=0, padx = 20, pady = 10, sticky="news")

    for widget in main_frame6.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    charge_on_threshold = tkinter.Label(main_frame6, text= "Charge On Threshold [in kW]")
    charge_on_threshold_var = tkinter.StringVar(main_frame6)
    charge_on_threshold_var.set("5.0")
    charge_on_threshold_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=charge_on_threshold_var)
    charge_on_threshold.grid(row=0,column=0)
    charge_on_threshold_box.grid(row=1, column =0)

    charge_off_threshold = tkinter.Label(main_frame6, text= "Charge Off Threshold [in kW]")
    charge_off_threshold_var = tkinter.StringVar(main_frame6)
    charge_off_threshold_var.set("7.0")
    charge_off_threshold_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=charge_off_threshold_var)
    charge_off_threshold.grid(row=0,column=1)
    charge_off_threshold_box.grid(row=1, column =1)

    discharge_off_threshold = tkinter.Label(main_frame6, text= "Discharge Off Threshold [in kW]")
    discharge_off_threshold_var = tkinter.StringVar(main_frame6)
    discharge_off_threshold_var.set("7.5")
    discharge_off_threshold_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=discharge_off_threshold_var)
    discharge_off_threshold.grid(row=0,column=2)
    discharge_off_threshold_box.grid(row=1, column =2)

    discharge_on_threshold = tkinter.Label(main_frame6, text= "Discharge On Threshold [in kW]")
    discharge_on_threshold_var = tkinter.StringVar(main_frame6)
    discharge_on_threshold_var.set("9.0")
    discharge_on_threshold_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=discharge_on_threshold_var)
    discharge_on_threshold.grid(row=4,column=0)
    discharge_on_threshold_box.grid(row=5, column =0)

    max_discharge_rate = tkinter.Label(main_frame6, text= "Max Discharge Rate [in kW]")
    max_discharge_rate_var = tkinter.StringVar(main_frame6)
    max_discharge_rate_var.set("1.0")
    max_discharge_rate_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=max_discharge_rate_var)
    max_discharge_rate.grid(row=4,column=1)
    max_discharge_rate_box.grid(row=5, column =1)

    max_charge_rate = tkinter.Label(main_frame6, text= "Max Charge Rate [in kW]")
    max_charge_rate_var = tkinter.StringVar(main_frame6)
    max_charge_rate_var.set("1.0")
    max_charge_rate_box = ttk.Spinbox(main_frame6, increment=0.1, textvariable=max_charge_rate_var)
    max_charge_rate.grid(row=4,column=2)
    max_charge_rate_box.grid(row=5, column =2)


    button = tkinter.Button(frame, text="Enter Data", command=enter_data)
    button.grid(row=6, column= 0, sticky="news", padx=20, pady=10)


    window.mainloop()   #ensures app runs

    return param_list