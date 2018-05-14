# Name: Nguyen Minh Thong Huynh
# ID: z5170141

import os, simulation as si


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
    os.chdir(os.getcwd()+"\sample_3") 
    no_tests = int(read_file_float("num_tests.txt")[0])
    for i in range(1,no_tests+1):
        mode = read_file_string("mode_{0}.txt".format(i))[0]
        para = read_file_float("para_{0}.txt".format(i))
        m = int(para[0])
        setup_time = para[1]
        delayedoff_time = para[2]

        if mode == 'random':
            time_end = para[3]
        else:
            time_end = None

        arrival = read_file_float("arrival_{0}.txt".format(i))
        service = read_file_float("service_{0}.txt".format(i))
        if mode == 'random':
            arrival = arrival[0]
            service = service[0]

        print ("Test {0}".format(i))
        print ("Mode: {0}".format(mode))
        print ("Number of Servers: {0}".format(m))
        print ("Setup time: {0}".format(setup_time))
        print ("Delayed off time: {0}".format(delayedoff_time))
        print ("Arrival time: {0}".format(arrival))
        print ("Service time: {0}".format(service))
        if mode == 'random':
            print ("Time end: {0}".format(time_end))

        (n_finish_jobs,mean_response_time) = si.simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end,i)
        # for i in range(int(delayedoff_time)):
        #     (n_finish_jobs,mean_response_time) = si.simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end,i)
        #     delayedoff_time -= 1

        

if __name__ == "__main__":
    main()