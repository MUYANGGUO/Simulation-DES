import numpy as np 
import math as math
import Vehicle
import os
import heapq
import sys
import Pedestrian

class Scene:
    def __init__(self,n,t,p,rng_seed):
        self.N = n #car
        self.P = p #people
        self.T = t
        self.rng_seed = rng_seed

    def vehicle_generate(self,time_stamp, car_type, car_direction, which_lane, ID):
        print('generating vehicles ... in the scene')
        numberOfCar = len(time_stamp)
        global_q_list = []
        # create 6 empty list for each lane
        for i in range(6):
            global_q_list.append([])
        # Every car is from either one of 6 directions below
        # N1 = [];
        # N2 = [];
        # N3 = [];
        # N4 = [];
        # E1 = [];
        # W1 = [];
        for i in range(numberOfCar):
            car_i = Vehicle.Vehicle((time_stamp[i]), car_type[i], car_direction[i], which_lane[i], ID[i])
            global_q_list[int(which_lane[i])].append(car_i)
        # add each car to certain lane

        # for i in range(6):  # heapify each lane
        #     heapq.heapify(global_q_list[i])

        return global_q_list

    def pedestrian_generate(self, time_stamp, ped_origin, ped_dest, ID):
        print('generating pedestrains ... in the scene')
        numberOfPedestrian = len(time_stamp)
        global_Pes_list = []

        for i in range(numberOfPedestrian):
            pedestrains_i = Pedestrian.Pedestrian(time_stamp[i], ped_origin[i], ped_dest[i], ID[i])
            global_Pes_list.append(pedestrains_i)
        heapq.heapify(global_Pes_list)
        return global_Pes_list

    def poisson_generate_timestamps(self):
        lamda = float(self.N)/float(self.T)/60.0/60.0 #per second
        Time = int(self.T*60.0*60.0) #total seond
        np.random.seed(self.rng_seed)
        poisson = np.random.poisson(lamda,Time)
        time_stamps = []
        time_stamp = 0.0
        for p in poisson:
            if p != 0:
                event_time = np.random.uniform(0,1.0,p)# per second, unit interval
                for t_s in event_time:
                    time_stamp=time_stamp+t_s
                    time_stamps.append(time_stamp)
            else:
                time_stamp = time_stamp+1.0
        np.sort(time_stamps)
        total_sim_event = len(time_stamps)
        sim_mean = np.mean(poisson)
        print('Based on input parameters [{} events , {} hr], expected rate is {:.3f} events/second, \nSampled {} events based on poisson process within time {} hr,sample mean is {:.3f} events/second\nNext start generating actors in the scene ...'\
            .format(self.N,self.T,lamda,total_sim_event,self.T,sim_mean))
        return time_stamps,poisson


    def poisson_generate_timestamps_people(self):
        lamda = float(self.P)/float(self.T)/60.0/60.0 #per second
        Time = int(self.T*60.0*60.0) #total seond
        np.random.seed(self.rng_seed)
        poisson = np.random.poisson(lamda,Time)
        time_stamps = []
        time_stamp = 0.0
        for p in poisson:
            if p != 0:
                event_time = np.random.uniform(0,1.0,p)# per second, unit interval
                for t_s in event_time:
                    time_stamp=time_stamp+t_s
                    time_stamps.append(time_stamp)
            else:
                time_stamp = time_stamp+1.0
        np.sort(time_stamps)
        total_sim_event = len(time_stamps)
        sim_mean = np.mean(poisson)
        print('Based on input parameters [{} events , {} hr], expected rate is {:.3f} events/second, \nSampled {} events based on poisson process within time {} hr,sample mean is {:.3f} events/second\nNext start generating actors in the scene ...'\
            .format(self.P,self.T,lamda,total_sim_event,self.T,sim_mean))
        return time_stamps,poisson
        
    

    


        
        


