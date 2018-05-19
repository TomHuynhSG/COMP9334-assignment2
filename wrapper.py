# Name: Nguyen Minh Thong Huynh
# ID: z5170141

import os, simulation as si
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

seed_start=5
seed_end=10
tc_trials=[0] #Default for only one Tc value run
#tc_trials=[0,3,7,9,10,11,12,13,15,17,20,25,30,40,50,100] #addition_to_paraTc
transient_cutoff_index = 1500
np.random.seed(seed_start)
DEBUG = False

# Try to use one at a time to display graph
DISPLAY_TRANSIENT_ONE_TC_GRAPH = False  #works well one tc_trials (the last element of tc_trials)
DISPLAY_RESPONSETIME_Tc_GRAPH = False
DISPLAY_SPREAD_DIFFERNT_Tc_GRAPH= False

def read_file_string(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [x.strip() for x in content] 
    return content

def read_file_float(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [float(x.strip()) for x in content] 
    return content

def main():
    os.chdir(os.getcwd()+"\sample_2") 
    no_tests = int(read_file_float("num_tests.txt")[0])
    for test in range(1,no_tests+1):
        mode = read_file_string("mode_{0}.txt".format(test))[0]
        para = read_file_float("para_{0}.txt".format(test))
        m = int(para[0])
        setup_time = para[1]
        delayedoff_time = para[2]

        if mode == 'random':
            time_end = para[3]
        else:
            time_end = None

        arrival = read_file_float("arrival_{0}.txt".format(test))
        service = read_file_float("service_{0}.txt".format(test))
        if mode == 'random':
            arrival = arrival[0]
            service = service[0]

        if DEBUG:
            print ("Test {0}".format(test))
            print ("Mode: {0}".format(mode))
            print ("Number of Servers: {0}".format(m))
            print ("Setup time: {0}".format(setup_time))
            print ("Delayed off time: {0}".format(delayedoff_time))
        if mode == 'random':
            arrival_rate = arrival
            service_rate = service
            if DEBUG:
                print ("Time end: {0}".format(time_end))
                print ("Arrival rate: {0}".format(arrival_rate))
                print ("Service rate: {0}".format(service_rate))
        else:
            if DEBUG:
                print ("Arrival time: {0}".format(arrival))
                print ("Service time: {0}".format(service))

        response_times_different_tc_seeds={}
        response_times_different_seeds_tc={}
        running_means_different_seeds_tc={}
        for seed in range(seed_start, seed_end+1):
            np.random.seed(seed)
            if DEBUG:
                print("SEED: "+str(seed))
            if mode == 'random':
                arrival=[]
                estimate_jobs = int(time_end) if arrival_rate<1 else int(arrival_rate*time_end)
                for a in range (estimate_jobs):
                    arrival.append(-math.log(1-np.random.rand())/arrival_rate)
                arrival = np.cumsum(arrival)
                arrival = [a for a in arrival if (a <= time_end)]
                arrival = [round(a,3) for a in arrival]
                service=[]
                
                for a in range(len(arrival)):
                    service.append (round(np.random.exponential(1.0/service_rate)+np.random.exponential(1.0/service_rate)+np.random.exponential(1.0/service_rate), 3))
            
            
            for new_tc in tc_trials:
                update_delayoff_time=delayedoff_time+new_tc

                # round up update delayoff_time
                if (mode == 'random') and (update_delayoff_time != 0.1):
                    update_delayoff_time = int(update_delayoff_time)

                if seed not in response_times_different_seeds_tc:
                    response_times_different_seeds_tc[seed]=[]


                if update_delayoff_time not in response_times_different_tc_seeds:
                    response_times_different_tc_seeds[update_delayoff_time]=[]
                    
                (n_finish_jobs, mean_response_time, response_times, running_means) = si.simulation(mode, arrival, service, m, setup_time, update_delayoff_time, time_end,test)

                stable_response_times = response_times[transient_cutoff_index:]
                mean_stable_response_time = sum(stable_response_times)/len(stable_response_times)

                response_times_different_tc_seeds[update_delayoff_time].append(mean_stable_response_time)
                response_times_different_seeds_tc[seed].append(mean_stable_response_time)
                running_means_different_seeds_tc[seed] = running_means


        # Graph Transient Behavior
        if DISPLAY_TRANSIENT_ONE_TC_GRAPH:
            print (running_means_different_seeds_tc)
            plt.title("Transient Behavior versus Steady State Behavior")
            plt.plot([], [], ' ', label="m = " + str(m) + ", setup_time = " + str(setup_time))
            plt.plot([], [], ' ', label="Tc = " + str(update_delayoff_time) + ", end_time = " + str(time_end))
            
            for seed_key in running_means_different_seeds_tc:
                plt.plot(running_means_different_seeds_tc[seed_key], label='running means for seed ='+str(seed_key))

            plt.xlabel('k', fontsize=15)
            plt.ylabel('Mean response time of first k jobs', fontsize=15)
            plt.legend()
            plt.show()
            
        #Graph Relationship between response time and Tc (delayoff_time)
        if DISPLAY_RESPONSETIME_Tc_GRAPH:
            plt.title("Relationship between response time and Tc (delayoff_time)")
            plt.plot([], [], ' ', label="m = " + str(m) + ", setup_time = " + str(setup_time))
            plt.plot([], [], ' ', label="end_time = " + str(time_end))
            
            for seed_key in response_times_different_seeds_tc:
                response_times_different_seeds_tc[seed_key]
                x=tc_trials
                plt.plot(x, response_times_different_seeds_tc[seed_key], label='response time for seed '+str(seed_key))

            #plt.axhline(y=[revise_mean_response_time], color='r', linestyle='-', label='Mean response time in stable period > k = 1500')

            plt.xlabel('Delayoff Time', fontsize=15)
            plt.ylabel('Mean response time', fontsize=15)
            plt.legend()
            plt.show()

        if DISPLAY_SPREAD_DIFFERNT_Tc_GRAPH:
            if DEBUG:
                print(response_times_different_tc_seeds)
            plt.title("The spread of mean response time for different Tc (delayoff_time)")
            plt.plot([], [], ' ', label="seed start = " + str(seed_start) + ", seed_end = " + str(seed_end))
            for delayoff_key in response_times_different_tc_seeds:
                response_times_per_tc = response_times_different_tc_seeds[delayoff_key]
                plt.scatter([delayoff_key]*len(response_times_per_tc), response_times_per_tc, label='response time for tc = '+str(delayoff_key))

                sample_mean = sum(response_times_per_tc)/len(response_times_per_tc)
                n = (seed_end-seed_start+1)
                sum_deviation = 0.0
                for i in response_times_per_tc:
                    sum_deviation+=(sample_mean-i)**2
                sample_standard_deviation = math.sqrt( sum_deviation/( n-1))  
                alpha = 0.05
                t_dis = t.ppf(1-alpha/2, (n-1))
                lower_bound = sample_mean - t_dis*sample_standard_deviation/math.sqrt(n)
                upper_bound = sample_mean + t_dis*sample_standard_deviation/math.sqrt(n)
                
                if DEBUG:
                    print("Tc :"+str(delayoff_key))
                    print("Lower Bound:" + str(lower_bound))
                    print("Sample Mean" + str(sample_mean))
                    print("Upper Bound" + str(upper_bound))

            plt.xlabel('Delayoff Time', fontsize=15)
            plt.ylabel('Mean response time', fontsize=15)
            plt.legend()
            plt.show()


if __name__ == "__main__":
    main()