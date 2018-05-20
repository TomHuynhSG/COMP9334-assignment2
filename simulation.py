# Name: Nguyen Minh Thong Huynh
# ID: z5170141
# Python 3.6.4 or Python 2.7.13

###################################################################################################
# This is helper simulation file for wrapper.py
# Do not run this file as main function
###################################################################################################


import heapq

# debug allowing functions to print out variable for debugging purpose
DEBUG = False

# boolean to write output files or not (speed up experiments or drawing graph)
WRITE_FILE = True


def find_longest_server_type(servers,events,type):
    final_id=None
    for id in servers:
        if servers[id]['status']==type:
            if (final_id==None):
                final_id= id
            else:
                if (find_server_time_type(events,id,type) > find_server_time_type(events,final_id,type)):
                    final_id = id
    return final_id

def find_server_time_type(events,server_id,type):
    for [e_time, e_type, e_id] in events:
        if (e_type==type) and (e_id==server_id):
            return e_time
    return None

def number_setup_servers(servers):
    n_setup_servers=0
    for id in servers:
        if servers[id]['status']=='setup':
            n_setup_servers+= 1
    return n_setup_servers

def number_marked_jobs(queue):
    n_marked_jobs=0
    for job in queue:
        if job['status']=='MARKED':
            n_marked_jobs+= 1
    return n_marked_jobs


def remove_event(events,type,id):
    for [e_time, e_type, e_id] in events:
        if (e_type==type and e_id==id):
            events.remove([e_time, e_type, e_id])
            heapq.heapify(events)

def wait_for_server(clock,servers,queue,events,job_id,setup_time):
    for id in servers:
        if servers[id]['status']=='off':
            servers[id]['status']='setup'
            heapq.heappush(events, [clock + setup_time, 'setup', id ] )
            queue.append({'id':job_id,'status':'MARKED'})
            return 'MARKED'

    #all server must be either busy or setup
    queue.append({'id':job_id,'status':'UNMARKED'})
    return 'UNMARKED'

def use_delay_server(clock,servers,jobs,events,server_id,job_id):
    remove_event(events,'delay',server_id)
    servers[server_id]['status']='busy'
    heapq.heappush(events, [clock+jobs[job_id]['service'], 'departure', [server_id,job_id] ] )

def use_free_server(clock,servers,jobs,events,server_id,job_id):
    servers[server_id]['status']='busy'
    heapq.heappush(events, [clock+jobs[job_id]['service'], 'departure', [server_id,job_id] ] )

def pop_first_marked(queue):
    for job in queue:
        if job['status']=='MARKED':
            queue.remove(job)
            return job
    return None

def find_first_unmarked(queue):
    for job in queue:
        if job['status']=='UNMARKED':
            return job
    return None


def simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end, test_no):
    clock = 0.0
    total_response_time=0.0

    departures=[]
    servers = {}
    jobs = {}
    queue = []
    events = []

    n_finish_jobs = 0
    n_jobs = len(arrival)
    

    # initialize servers
    for i in range(1,m+1):
        servers[i]={'status':'off'}  #server status based on server its id (off,busy,setup,delay)
    
    # initialize job rerference array (this array will be fixed) from arrival arrays
    for i in range(n_jobs):
        jobs[i+1]={"arrival":arrival[i],"service":service[i]}
    
    # initialize arrival events (arrival_time, event_type, related_id) 
    for id in jobs:
        heapq.heappush(events, [jobs[id]['arrival'], 'arrival', id ] )

    while len(events)!=0:
        # pop out a event which has soonest starting time 
        [e_time, e_type, e_id]=heapq.heappop(events)
        
        # update master clock
        clock=e_time

        assert(number_setup_servers(servers)==number_marked_jobs(queue))
        
        # stop simulaion when time exceeds time end
        if (mode == 'random') and (clock>time_end):
            break
        
        # handle arrival event
        if e_type=='arrival':
            job_id = e_id
            free_server_id = find_longest_server_type(servers,events,'delay')
            if free_server_id==None:
                wait_for_server(clock,servers,queue,events,job_id,setup_time)
            else:
                use_delay_server(clock,servers,jobs,events,free_server_id,job_id)
        
        # handle departure event
        if e_type=='departure':
            [server_id, job_id] = e_id
            departures.append([jobs[job_id]['arrival'],clock])
            n_finish_jobs+= 1

            if len(queue)==0:
                servers[server_id]['status']='delay'
                heapq.heappush(events, [clock + delayedoff_time, 'delay', server_id ] )
            else:
                job = queue.pop(0)
                use_free_server(clock,servers,jobs,events,server_id,job['id'])
                if job['status']=='MARKED':
                    unmarked_job = find_first_unmarked(queue)
                    if (unmarked_job == None):
                        setup_server_id = find_longest_server_type(servers,events,'setup')
                        servers[setup_server_id]['status']='off'
                        remove_event(events,'setup',setup_server_id)
                    else:
                        unmarked_job['status'] = 'MARKED'

        # handle setup event
        if e_type=='setup':
            server_id = e_id
            job = pop_first_marked(queue)
            use_free_server(clock,servers,jobs,events, server_id, job['id'])
        
        # handle delay event
        if e_type=='delay':
            server_id=e_id
            servers[server_id]['status']='off'
    

    running_times = []
    running_means = []
    response_times = []

    
    for departure in departures:
        response_times.append(departure[1] - departure[0])
    
    total_response_time = sum(response_times)
    mean_response_time = total_response_time/n_jobs


    for i in range(len(response_times)):
        if i == 0:
            running_times.append(response_times[i])
        else:
            running_times.append(running_times[-1]+response_times[i])
    
    for i in range(len(running_times)):
        running_means.append(running_times[i]/(i+1))

    if DEBUG:
        print ("Mean Response Time: {0:.3f}".format(mean_response_time))
    
    if WRITE_FILE:
        with open('mrt_{0}.txt'.format(test_no), 'w') as output_file:
            output_file.write("{0:.3f}".format(mean_response_time))


    departures.sort(key=lambda x: x[1])

    if WRITE_FILE:
        output_file = open('departure_{0}.txt'.format(test_no),"w")
        for i in range(n_finish_jobs):
            output_file.write("{0:.3f}\t{1:.3f}\n".format(departures[i][0],departures[i][1]))
        output_file.close() 

    return  (n_finish_jobs,mean_response_time,response_times,running_means)