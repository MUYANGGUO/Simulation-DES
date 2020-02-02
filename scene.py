import numpy as np 
import math as math
import os

class Scene:
    dirpath = os.path.dirname(os.path.realpath(__file__))
    def __init__(self,n,t):
        self.N = n
        self.T = t
    def vehicle_generate(self):
        print('generating vehicles ... in the scene')
    def pedestrain_generate(self):
        print('generating pedestrains ... in the scene')

    def poisson_generate_timestamps(self):
        lamda = float(self.N)/float(self.T)/60.0/60.0 #per second
        Time = int(self.T*60.0*60.0) #total seonds
        poisson = np.random.poisson(lamda,Time)

        time_stamps = []
        time_stamp = 0.0
        # print(np.mean(poisson))
        for p in poisson:
            if p != 0:
                event_time = np.random.uniform(0,1.0,p)# per second, unit minute interval
                for t_s in event_time:
                    time_stamp=time_stamp+t_s;
                    time_stamps.append(time_stamp)
            else:
                time_stamp = time_stamp+1.0
        np.sort(time_stamps)
        total_sim_event = len(time_stamps)
        # print(time_stamps)
        # print(len(time_stamps))
        # print(time_stamps[-1]/60/60)
        print('generated timestamps for input parameters [{} events , {} hr]...\nSampled {} events based on poisson process within time {} hr'.format(self.N,self.T,total_sim_event,self.T))
        return time_stamps
    


        
        


