import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def data_form():
    window = tkinter.Tk()  #main window
    window.title("Input Parameters for Simulation")

    def enter_data():
        #glmfile = openglm.get()
        #tmy2file = opentmy.get()
        tlength = time_spinbox.get()
        #starttime = 
        #stoptime =
        p1 = pi1_var.get()
        p2 = pi2_var.get()
        p3 = pi3_var.get()
        p4 = pi4_var.get()
        p5 = pi5_var.get()
        DER_pen = res_DER_spinbox.get()
        install = lc_install_box.get()
        peff = PV_eff_spinbox.get()
        Parea = PV_entrybox.get()
        ev = EV_charger_box.get()
        beff = bat_eff_box.get()
        bcap = bat_cap_box.get()
        ieff = inv_eff_box.get()
        ipow = inv_pow_box.get()
        ipf = inv_pf_box.get()

        #print("Chosen .glm file:", glmfile, "Chosen .tmy2 file: ", tmy2file)
        print("Time-step Length:", tlength, "Start Time:", "Stop Time:", )
        print("Chosen Perfomance Indices:", p1,p2,p3,p4,p5)
        print("Residential DER Penetration:", DER_pen, "Large Scale Installation:", install, "PV efficiency:", peff, "PV Area:", Parea, )
        print("Battery Efficiency:", beff, "Battery Capacity:", bcap,"EV Charger Type:", ev)
        print("Inverter Efficiency:", ieff, "Inverter Rated Power:", ipow, "Inverter Power Factor:", ipf)
        print("------------------------------------------------------")

        #closes window so that program can continue
        window.quit()

    






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
        glm_file = fd.askopenfilename(title ='Open a file (.glm file)', initialdir='/',filetypes=glmfiletypes)
        showinfo(title="Selected File", message=glm_file)
    openglm = ttk.Button(main_frame1, text='Choose a file', command=select_file)
    openglm.grid(row=0, column=1, sticky ='news',pady=10)

    #tmy file reader
    tmy_title = tkinter.Label(main_frame1, text = "Please select a .tmy2 file")
    tmy_title.grid(row=1,column=0, pady=10)
    def select_file():
        tmyfiletypes = (
            ('tmy2 files', '*.tmy2'),
            ('tmy3 files', '*.tmy3'),
            ('All files', '*.*')
        )
        tmy_file = fd.askopenfilename(title ='Open a file (.tmy2 file)', initialdir='/',filetypes=tmyfiletypes)
        showinfo(title="Selected File", message=tmy_file)
    opentmy = ttk.Button(main_frame1, text='Choose a file', command=select_file)
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

    start_time = tkinter.Label(main_frame2, text = "Choose a start time [yyyy-mm-dd hr:mm:ss]")

    stop_time = tkinter.Label(main_frame2, text="Choose a stop time")

    start_time.grid(row=0,column=1)

    stop_time.grid(row=0, column=2)


    #main frame section 3
    main_frame3 = tkinter.LabelFrame(frame, text = "Select any/all performance indicators you would like to assess (pick atleast 1)")
    main_frame3.grid(row = 2, column=0, padx = 20, pady = 10, sticky="news")
    for widget in main_frame3.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    pi1_var = tkinter.StringVar(value= "Not selected")
    performance1_check = tkinter.Checkbutton(main_frame3,text = "ANSI Voltage Standard", variable = pi1_var, onvalue="Selected" , offvalue="Not Selected")
    performance1_check.grid(row=0,column=1)

    pi2_var = tkinter.StringVar(value= "Not selected")
    performance2_check = tkinter.Checkbutton(main_frame3,text = "Overcurrent and Overloading", variable = pi2_var, onvalue="Selected" , offvalue="Not Selected")
    performance2_check.grid(row=1,column=1)

    pi3_var = tkinter.StringVar(value= "Not selected")
    performance3_check = tkinter.Checkbutton(main_frame3,text = "Voltage Unbalance", variable = pi3_var, onvalue="Selected" , offvalue="Not Selected")
    performance3_check.grid(row=2,column=1)

    pi4_var = tkinter.StringVar(value= "Not selected")
    performance4_check = tkinter.Checkbutton(main_frame3,text = "Losses in Line", variable = pi4_var, onvalue="Selected" , offvalue="Not Selected")
    performance4_check.grid(row=3,column=1)

    pi5_var = tkinter.StringVar(value= "Not selected")
    performance5_check = tkinter.Checkbutton(main_frame3,text = "Power Flow in Substation Transformers", variable = pi5_var, onvalue="Selected" , offvalue="Not Selected")
    performance5_check.grid(row=4,column=1)


    #main frame section 4
    main_frame4 = tkinter.LabelFrame(frame, text = "Select a value for the following parameters")
    main_frame4.grid(row = 3, column=0, padx = 20, pady = 10, sticky="news")
    for widget in main_frame4.winfo_children():
        widget.grid_configure(padx=10, pady=5)


    res_DER_pen = tkinter.Label(main_frame4, text = 'Residential DER Penetration [0,1]')
    res_DER_spinbox = tkinter.Spinbox(main_frame4, from_=0, to_=1, increment=0.1)
    res_DER_pen.grid(row=0, column=0)
    res_DER_spinbox.grid(row=1, column=0)

    lc_install = tkinter.Label(main_frame4, text="Large-Scale Installation")
    lc_install_box = ttk.Combobox(main_frame4, values = ["None", "PV-Cells", "Battery Storage", "Both"])
    lc_install.grid(row =0, column=1)
    lc_install_box.grid(row=1, column=1)

    PV_eff = tkinter.Label(main_frame4, text = 'PV Efficiency [0,1]')
    PV_eff_var = tkinter.StringVar(main_frame4)
    PV_eff_var.set("0.15")
    PV_eff_spinbox = tkinter.Spinbox(main_frame4, from_=0, to_=1, increment=0.05, textvariable=PV_eff_var)
    PV_eff.grid(row=0, column=2)
    PV_eff_spinbox.grid(row=1, column=2)

    PV_area = tkinter.Label(main_frame4, text = "PV Area")
    PV_area_var=tkinter.StringVar(main_frame4)
    PV_area_var.set("2500")
    PV_entrybox = tkinter.Entry(main_frame4, textvariable=PV_area_var)
    PV_area.grid(row=2, column=1)
    PV_entrybox.grid(row = 3, column=1)

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

    bat_cap = tkinter.Label(main_frame5, text = "Battery Capacity")
    bat_cap_var=tkinter.StringVar(main_frame5)
    bat_cap_var.set("1000")
    bat_cap_box = tkinter.Entry(main_frame5, textvariable=bat_cap_var)
    bat_cap.grid(row=2, column=0)
    bat_cap_box.grid(row = 3, column=0)

    EV_charger = tkinter.Label(main_frame5, text= "EV Charger Type")
    EV_charger_box = ttk.Combobox(main_frame5, values=["LOW","MEDIUM","HIGH"])
    EV_charger.grid(row=4,column = 0)
    EV_charger_box.grid(row=5, column =0)

    inv_eff=tkinter.Label(main_frame5, text="Inverter Efficiency")
    inv_eff_var=tkinter.StringVar(main_frame5)
    inv_eff_var.set("0.90")
    inv_eff_box=ttk.Spinbox(main_frame5, from_=0, to_=1, increment=0.01, textvariable=inv_eff_var)
    inv_eff.grid(row=0, column=1)
    inv_eff_box.grid(row=1, column=1)

    inv_pow= tkinter.Label(main_frame5, text = "Inverter Rated Power")
    inv_pow_var=tkinter.StringVar(main_frame5)
    inv_pow_var.set("100 000")
    inv_pow_box=ttk.Spinbox(main_frame5, from_=0, to_=200000, increment=1000, textvariable=inv_pow_var)
    inv_pow.grid(row= 2, column =1)
    inv_pow_box.grid(row=3, column=1)

    inv_pf= tkinter.Label(main_frame5, text= "Inverter Power Factor [0,1]") 
    inv_pf_var=tkinter.StringVar(main_frame5)
    inv_pf_var.set=("1.00")
    inv_pf_box=ttk.Spinbox(main_frame5,from_=0, to_=1, increment=0.01, textvariable=inv_pf_var)
    inv_pf.grid(row =4, column=1)
    inv_pf_box.grid(row=5, column =1)


    button = tkinter.Button(frame, text="Enter Data", command=enter_data)
    button.grid(row=5, column= 0, sticky="news", padx=20, pady=10)


    window.mainloop()   #ensures app runs

    print("Data form exited")