# Name: Nguyen Minh Thong Huynh
# ID: z5170141

#mode # random or trace
#arrival  #lamda #arrival rate of the jobs
#service  #mu 
#m #number of servers
#setup_time
#delayedoff_time #Tc
#time_end #stops the simulation if the master clock exceeds this value

def simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end="Na"):
    master_clock = 0.0
    
    #output 2 files
    pass