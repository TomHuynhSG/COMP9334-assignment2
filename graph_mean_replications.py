import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import t

def read_departure_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [x.strip() for x in content] 
    return content

def main():
    os.chdir(os.getcwd()+"\sample_0_Tc_01")
    m=5
    setup_time = 5
    arrival_rate = 0.35
    service_rate = 1
    seed_start=5
    seed_end=7
    delayedoff_time=0.1
    time_end=20000
    cutoff_index=1500
    plt.title("Mean response time in stable part of Tc = 0.1 for different seeds")
    #plt.title("Steady State Behavior")
    plt.plot([], [], ' ', label="m = " + str(m) + ", setup_time = " + str(setup_time) + ", lamda = "+str(arrival_rate)+", mu = "+str(service_rate))
    plt.plot([], [], ' ', label="Tc = " + str(delayedoff_time) + ", end_time = " + str(time_end) + ", seed = "+str(seed_start)+"->"+str(seed_end))
    
    mean_stable_response_times=[]
    for seed in range(seed_start,seed_end+1):
        print ("Seed {0}".format(seed))

        departures = read_departure_file("departure_seed_{0}.txt".format(seed))
        response_times=[]
        running_times = []
        running_means = []

        for i in range(len(departures)):
            departures[i] = [float(x) for x in departures[i].split()]
            
        

        for departure in departures:
            response_times.append(departure[1] - departure[0])

        # mean_response_time = sum(response_times)/len(response_times)
        # print ("mean_response_time {0}".format(mean_response_time))
        stable_response_times = response_times[cutoff_index:]
        mean_stable_response_time = sum(stable_response_times)/len(stable_response_times)

        mean_stable_response_times.append(mean_stable_response_time)
        
        plt.scatter(0.1, mean_stable_response_time, label='response time for seed = '+str(seed))

    sample_mean = sum(mean_stable_response_times)/len(mean_stable_response_times)
    n = (seed_end-seed_start+1)
    sum_deviation = 0.0
    for i in mean_stable_response_times:
        sum_deviation+=(sample_mean-i)**2
    sample_standard_deviation = math.sqrt( sum_deviation/( n-1))  
    alpha = 0.05
    t_dis = t.ppf(1-alpha/2, (n-1))
    lower_bound = sample_mean - t_dis*sample_standard_deviation/math.sqrt(n)
    upper_bound = sample_mean + t_dis*sample_standard_deviation/math.sqrt(n)
    print(lower_bound)
    print(upper_bound)
    # plt.axvline(x=cutoff_index, label = 'transient removal line k = 1500')
    # plt.xlabel('k', fontsize=15)
    plt.gca().axes.set_xlim([0,2])
    plt.ylabel('Mean response time', fontsize=15)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()