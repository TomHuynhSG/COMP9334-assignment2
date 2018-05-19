# Name: Nguyen Minh Thong Huynh
# ID: z5170141

import os, simulation as si
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

###################################################################################################
# Main python file to run
# Every important parameter might be needed to changed are on the header right below
# The default parameters will do exactly what the spec requires but nothing more
# For more functionalities and graph analysis, enable more parameters on the headers
# Try to use only one displaying graph function at a time to display different graphs
#
###################################################################################################


# seed start and end will define a range of seed for the program to run
# Note: to run 1 seed then put both numbers to be the same
seed_start=5
seed_end=5

# how much Tc will be increase from default Tc from para to try
# Note: they will be addition to input Tc
# if only use input Tc, put [0]
tc_trials=[0]
#tc_trials=[0,3,7,9,10,11,12,13,15,17,20,25,30,40,50,100] #full_experiment for a variety of Tc

np.random.seed(seed_start)

#max index where transident part will be remove from response time array
transient_cutoff_max=1500

# debug allowing functions to print out variable for debugging purpose
DEBUG = False

# Try to use only one at a time to display different graphs
# display transient graph for one Tc from different seeds
DISPLAY_TRANSIENT_ONE_TC_GRAPH = False  # only works well one element tc_trials like [0] or [20]

# display graph showing how response time changes based on Tc
DISPLAY_RESPONSETIME_Tc_GRAPH = False 

# display graph showing spread of mean response times for each Tc at different seeds
DISPLAY_SPREAD_DIFFERNT_Tc_GRAPH= False

# calculate the spread of a paired-t confidence interval between baseline system and compared system
CALCULATE_DIFFERENCE_SPREAD = False

# Confidence interval parameter for t-student distribution
ALPHA = 0.05

# read strings from file
def read_file_string(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [x.strip() for x in content] 
    return content

# read float numbers from file
def read_file_float(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [float(x.strip()) for x in content] 
    return content

def main():
    os.chdir(os.getcwd()+"\sample_2")

    no_tests = int(read_file_float("num_tests.txt")[0])11
    for test in range(1,no_tests+1):

        # read input mode
        mode = read_file_string("mode_{0}.txt".format(test))[0]
        
        # read input paras
        para = read_file_float("para_{0}.txt".format(test))
        m = int(para[0])
        setup_time = para[1]
        delayedoff_time = para[2]

        if mode == 'random':
            time_end = para[3]
        else:
            time_end = None

        # read input arrival and service
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

        # variable to store values from simulation to draw graph and calculate spread
        # response times of each tc for different seeds
        response_times_different_tc_seeds={}

        # response times of each seeds for different tc
        response_times_different_seeds_tc={}

        # running means of each seeds for different tc     
        running_means_different_seeds_tc={}

        for seed in range(seed_start, seed_end+1):
            # assign seed to random generator
            np.random.seed(seed)
            if DEBUG:
                print("SEED: "+str(seed))
            if mode == 'random':
                arrival=[]
                #estimate number of jobs based on time end to make sure it generate enough
                estimate_jobs = int(time_end) if arrival_rate<1 else int(arrival_rate*time_end)
                
                # generate random arrival events
                for a in range (estimate_jobs):
                    arrival.append(-math.log(1-np.random.rand())/arrival_rate)
                arrival = np.cumsum(arrival)
                arrival = [a for a in arrival if (a <= time_end)]
                arrival = [round(a,3) for a in arrival]
                
                #generate random service events
                service=[]
                for a in range(len(arrival)):
                    service.append (round(np.random.exponential(1.0/service_rate)+np.random.exponential(1.0/service_rate)+np.random.exponential(1.0/service_rate), 3))
            
            for new_tc in tc_trials:
                
                # get new delayoff_time based on tc trial array to try out different tc
                update_delayoff_time=delayedoff_time+new_tc

                # round up update delayoff_time (optional) 
                if (mode == 'random') and (update_delayoff_time != 0.1):
                    update_delayoff_time = int(update_delayoff_time)

                # initialize for special arrays mentioned above
                if seed not in response_times_different_seeds_tc:
                    response_times_different_seeds_tc[seed]=[]
                if update_delayoff_time not in response_times_different_tc_seeds:
                    response_times_different_tc_seeds[update_delayoff_time]=[]
                
                # simulation starts
                (n_finish_jobs, mean_response_time, response_times, running_means) = si.simulation(mode, arrival, service, m, setup_time, update_delayoff_time, time_end,test)

                # make sure we have enough jobs to cutoff like intended
                if len(response_times) > transient_cutoff_max:
                    transient_cutoff_index = transient_cutoff_max
                else:
                    transient_cutoff_index = 0

                # calculate mean stable response times in stable part
                stable_response_times = response_times[transient_cutoff_index:]
                mean_stable_response_time = sum(stable_response_times)/len(stable_response_times)

                # store these info about response times to arrays to draw graphs or calculate spread later
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

        # display graph showing spread of mean response times for each Tc at different seeds
        if DISPLAY_SPREAD_DIFFERNT_Tc_GRAPH:
            if DEBUG:
                print(response_times_different_tc_seeds)
            plt.title("The spread of mean response time for different Tc (delayoff_time)")
            plt.plot([], [], ' ', label="seed start = " + str(seed_start) + ", seed_end = " + str(seed_end))
            for delayoff_key in response_times_different_tc_seeds:
                response_times_per_tc = response_times_different_tc_seeds[delayoff_key]
                plt.scatter([delayoff_key]*len(response_times_per_tc), response_times_per_tc, s=[5]*len(response_times_per_tc), label='response time for tc = '+str(delayoff_key))

                sample_mean = sum(response_times_per_tc)/len(response_times_per_tc)
                n = (seed_end-seed_start+1)
                sum_deviation = 0.0
                for i in response_times_per_tc:
                    sum_deviation+=(sample_mean-i)**2
                sample_standard_deviation = math.sqrt( sum_deviation/( n-1))  
                t_dis = t.ppf(1-ALPHA/2, (n-1))
                lower_bound = sample_mean - t_dis*sample_standard_deviation/math.sqrt(n)
                upper_bound = sample_mean + t_dis*sample_standard_deviation/math.sqrt(n)
                
                if DEBUG:
                    print ("Spread of a Tc")
                    print("Tc :"+str(delayoff_key))
                    print("Lower Bound:" + str(lower_bound))
                    print("Sample Mean" + str(sample_mean))
                    print("Upper Bound" + str(upper_bound))

            plt.xlabel('Delayoff Time', fontsize=15)
            plt.ylabel('Mean response time', fontsize=15)
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.show()

        # calculate the spread of a paired-t confidence interval between baseline system and compared system
        if CALCULATE_DIFFERENCE_SPREAD:

            #Assume the first one is baseline and exist
            baseline_mrts = response_times_different_tc_seeds[0.1] 
            for delayoff_key in response_times_different_tc_seeds:
                compare_mrts = response_times_different_tc_seeds[delayoff_key]
                assert (len(baseline_mrts)==len(compare_mrts))
                difference_mrts=[]
                for i in range(len(baseline_mrts)):
                    difference_mrts.append(compare_mrts[i] - baseline_mrts[i])

                sample_mean = sum(difference_mrts)/len(difference_mrts)
                n = (seed_end-seed_start+1)
                sum_deviation = 0.0
                for difference_mrt in difference_mrts:
                    sum_deviation+=(sample_mean-difference_mrt)**2
                sample_standard_deviation = math.sqrt( sum_deviation/( n-1))  
                t_dis = t.ppf(1-ALPHA/2, (n-1))
                lower_bound = sample_mean - t_dis*sample_standard_deviation/math.sqrt(n)
                upper_bound = sample_mean + t_dis*sample_standard_deviation/math.sqrt(n)
                if DEBUG:
                    print ("Spread difference from the baseline")
                    print("Tc :"+str(delayoff_key))
                    print("Lower Bound:" + str(lower_bound))
                    print("Sample Mean" + str(sample_mean))
                    print("Upper Bound" + str(upper_bound))

if __name__ == "__main__":
    main()