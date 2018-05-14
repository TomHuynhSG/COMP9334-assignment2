# Name: Nguyen Minh Thong Huynh
# ID: z5170141

#mode # random or trace
#arrival  #lamda #arrival rate of the jobs
#service  #mu 
#m #number of servers
#setup_time
#delayedoff_time #Tc
#time_end #stops the simulation if the master clock exceeds this value


import heapq
import numpy as np
np.random.seed(1)

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
    for [time, e_Type, event] in events:
        if (event['type']==type) and (event['id']==server_id):
            return time
    return None

def remove_event(events,type,id):
    for [time, e_type, event] in events:
        if (event['type']==type and event['id']==id):
            events.remove([time, e_type,event])
            heapq.heapify(events)

def wait_for_server(clock,servers,queue,events,job_id,setup_time):
    for id in servers:
        if servers[id]['status']=='off':
            servers[id]['status']='setup'
            heapq.heappush(events, [clock + setup_time, 'setup' ,{'type':'setup', 'id':id}    ] )
            queue.append({'id':job_id,'status':'MARKED'})
            return 'MARKED'

    #all server must be either busy or setup
    queue.append({'id':job_id,'status':'UNMARKED'})
    return 'UNMARKED'

def use_delay_server(clock,servers,jobs,events,server_id,job_id):
    remove_event(events,'delay',server_id)
    servers[server_id]['status']='busy'
    heapq.heappush(events, [clock+jobs[job_id]['service'], 'departure',{'type':'departure', 'id':[server_id,job_id]} ] )

def use_free_server(clock,servers,jobs,events,server_id,job_id):
    servers[server_id]['status']='busy'
    heapq.heappush(events, [clock+jobs[job_id]['service'], 'departure',{'type':'departure', 'id':[server_id,job_id]} ] )

def pop_first_marked(queue):
    for job in queue:
        if job['status']=='MARKED':
            queue.remove(job)
            return job

def simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end, test_no):
    clock = 0.0
    total_response_time=0.0


    if mode == 'random':
        arrival_rate = arrival
        service_rate = service
        arrival = np.random.poisson(1/arrival_rate, int(time_end))
        arrival = np.cumsum(arrival)
        arrival = [a for a in arrival if (a <= time_end)]     
        n_jobs = len(arrival)
        service=[]
        
        for i in range(n_jobs):
            service.append (round(np.random.exponential(scale=1/service_rate)+np.random.exponential(scale=1/service_rate)+np.random.exponential(scale=1/service_rate), 3))
        
        arrival = [10, 24, 34, 48, 60, 77, 91, 105, 115]
        service = [12.669, 7.333, 6.527, 6.911, 5.79, 4.087, 4.013, 5.917, 5.134]
        n_jobs = len(arrival)
        print ("Random arrival: {0}".format(arrival))
        print ("Random servive: {0}".format(service))


    else: 
        n_jobs = len(arrival)
    
    departures=[]

    servers = {}
    jobs = {}
    queue = []
    events = []
    n_finish_jobs = 0
    
    
    
    
    # events { time : ? ,type: "arrive, depart, setup, delay"}

    # initialize servers
    for i in range(1,m+1):
        servers[i]={'status':'off'}  #server status based on server its id (off,busy,setup,delay)
    
    # initialize jobs
    for i in range(n_jobs):
        jobs[i+1]={"arrival":arrival[i],"service":service[i]}
    
    # initialize arrival events
    for id in jobs:
        heapq.heappush(events, [jobs[id]['arrival'], 'arrival', {'type':'arrival', 'id':id}    ] )

    print(servers)
    print(jobs)
    print(events)
    
    while len(events)!=0:
        [time, e_type, event]=heapq.heappop(events)
        clock=time
        if (mode == 'random') and (clock>time_end):
            break
        if event['type']=='arrival':
            job_id = event['id']
            free_server_id = find_longest_server_type(servers,events,'delay')
            if free_server_id==None:
                wait_for_server(clock,servers,queue,events,job_id,setup_time)
            else:
                use_delay_server(clock,servers,jobs,events,free_server_id,job_id)
        
        if event['type']=='departure':
            [servers_id,job_id] = event['id']
            departures.append(clock)
            total_response_time += clock - jobs[job_id]['arrival']
            n_finish_jobs+= 1

            if len(queue)==0:
                servers[servers_id]['status']='delay'
                heapq.heappush(events, [clock+delayedoff_time, 'delay',{'type':'delay', 'id':server_id} ] )
            else:
                job = queue.pop(0)
                use_free_server(clock,servers,jobs,events,server_id,job['id'])
                if job['status']=='MARKED':
                    setup_server_id = find_longest_server_type(servers,events,'setup')
                    servers[setup_server_id]['status']='off'
                    remove_event(events,'setup',setup_server_id)


        if event['type']=='setup':
            server_id=event['id']
            job = pop_first_marked(queue)
            use_free_server(clock,servers,jobs,events,server_id,job['id'])
        
        if event['type']=='delay':
            server_id=event['id']
            servers[server_id]['status']=='off'
    #output 2 files

    mean_response_time = total_response_time/n_jobs
    print ("Mean Response Time: {0:.3f}".format(mean_response_time))
    with open('mrt_{0}.txt'.format(test_no), 'w') as output_file:
        output_file.write("{0:.3f}".format(mean_response_time))

    output_file = open('departure_{0}.txt'.format(test_no),"w") 
    for i in range(n_finish_jobs):
        print ("{0:.3f}\t{1:.3f}".format(arrival[i],departures[i]))
        output_file.write("{0:.3f}\t{1:.3f}\n".format(arrival[i],departures[i]))
    output_file.close() 

    return  (n_finish_jobs,mean_response_time)