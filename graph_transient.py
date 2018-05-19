import os
import matplotlib.pyplot as plt
import numpy as np

def read_departure_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [x.strip() for x in content] 
    return content

def main():
    os.chdir(os.getcwd()+"\sample_0")
    m=5
    setup_time = 5
    arrival_rate = 0.35
    service_rate = 1
    seed_start=5
    seed_end=9
    delayedoff_time=0.1
    time_end=20000
    cutoff_index=1500
    plt.title("Transient Behavior versus Steady State Behavior")
    #plt.title("Steady State Behavior")
    plt.plot([], [], ' ', label="m = " + str(m) + ", setup_time = " + str(setup_time) + ", lamda = "+str(arrival_rate)+", mu = "+str(service_rate))
    plt.plot([], [], ' ', label="Tc = " + str(delayedoff_time) + ", end_time = " + str(time_end) + ", seed = "+str(seed_start)+"->"+str(seed_end))
    
    for seed in range(seed_start,seed_end+1):
        print ("Seed {0}".format(seed))

        departures = read_departure_file("departure_seed_{0}.txt".format(seed))
        response_times=[]
        running_times = []
        running_means = []

        for t in range(len(departures)):
            departures[t] = [float(x) for x in departures[t].split()]
            
        

        for departure in departures:
            response_times.append(departure[1] - departure[0])

        # mean_response_time = sum(response_times)/len(response_times)
        # print ("mean_response_time {0}".format(mean_response_time))
        # stable_response_times = response_times[cutoff_index:]
        # mean_stable_response_time = sum(stable_response_times)/len(stable_response_times)
        # print ("mean_stable_response_time {0}".format(mean_stable_response_time))
        # print ("Difference {0}".format(mean_stable_response_time-mean_response_time))

        for i in range(len(response_times)):
            if i == 0:
                running_times.append(response_times[i])
            else:
                running_times.append(running_times[-1]+response_times[i])

        for i in range(len(running_times)):
            running_means.append(running_times[i]/(i+1))

        x = np.arange(1, len(running_means)+1)
        plt.plot(x, running_means, label='running means seed = '+str(seed))

    plt.axvline(x=cutoff_index, label = 'transient removal line k = 1500')
    plt.xlabel('k', fontsize=15)
    plt.ylabel('Mean response time of first k jobs', fontsize=15)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()