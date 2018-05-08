# Name: Nguyen Minh Thong Huynh
# ID: z5170141

import os, simulation as si

def read_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    #whitespace
    content = [x.strip() for x in content] 
    return content

def main():
    os.chdir(os.getcwd()+"\COMP9334-assignment2\sample_1") 
    no_tests = int(read_file("num_tests.txt")[0])
    for i in range(1,no_tests+1):
        mode = read_file("mode_{0}.txt".format(i))[0]
        para = read_file("para_{0}.txt".format(i))
        m = int(para[0])
        setup_time = float(para[1])
        delayedoff_time = float(para[2])

        arrival = read_file("arrival_{0}.txt".format(i))
        service = read_file("service_{0}.txt".format(i))

        print ("Test {0}".format(i))
        print ("Mode: {0}".format(mode))
        print ("Number of Servers: {0}".format(m))
        print ("Setup time: {0}".format(setup_time))
        print ("Delayed off time: {0}".format(delayedoff_time))
        print ("Arrival time: {0}".format(arrival))
        print ("Service time: {0}".format(service))
        print()
        si.simulation(mode, arrival, service, m, setup_time, delayedoff_time)
        

if __name__ == "__main__":
    main()