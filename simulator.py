import os
import collections
import argparse
import multiprocessing
import json
import time
from random import randint
import numpy as np
import math as mathå
import mpl_toolkits.mplot3d
import matplotlib
import matplotlib.pyplot as plt
import TrafficLight as tl
from scene import Scene
import server as sr

_author_  = 'Muyang Guo, Wei Zhao, Shushu Zhao, Wenyue Wang'

def parseArguments():
    '''

    simulation time:

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('total_events', help = ':indicate the total events would like to simulate, requested here', type=float, default = 100)
    parser.add_argument('total_people', help = ':indicate the total people would like to simulate, requested here', type=float, default = 100)
    parser.add_argument('simulation_time', help = ':indicate simulation duration time, unit is hour, requested here', type=float, default = 1)

    args = parser.parse_args()
    return args

def save_timestamps_plot(time_stamps,id_list,name):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    res_dir = results_dir = os.path.join(dirpath, 'outputs/')
    if not os.path.isdir(res_dir):
        os.makedirs(res_dir)
    print("saving ... {} plot ... ".format(name))
    x = time_stamps
    y = id_list
    fig, ax = plt.subplots()
    plt.title(name)
    plt.ylabel('Events')
    plt.xlabel('Time in (s)')
    ax.scatter(x, y,marker="|",s=30)
    ax.scatter(x, y,marker="_",color='r', label=name+'(arrival)',s=3)
    ax.legend()
    plt.savefig(res_dir+name+'.png',dpi=600)
    return

def save_poisson_hist_plot(poisson,name):
    print("saving ... {} plot ... ".format(name)) 
    dirpath = os.path.dirname(os.path.realpath(__file__))
    res_dir = results_dir = os.path.join(dirpath, 'outputs/')
    if not os.path.isdir(res_dir):
        os.makedirs(res_dir)
    fig, ax = plt.subplots()
    plt.title(name)
    plt.ylabel('count')
    plt.xlabel('bins')
    bin_num = (max(poisson)-min(poisson))*4
    n, bins, patches = plt.hist(poisson,bin_num, facecolor='b', alpha=0.75)
    plt.savefig(res_dir+name+'.png',dpi=600)
    return

def compare_timestamps_plot(time_stamps_1,id_list_1,time_stamps_2,id_list_2,name):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    res_dir = results_dir = os.path.join(dirpath, 'outputs/')
    if not os.path.isdir(res_dir):
        os.makedirs(res_dir)
    print("saving ... {} plot ... ".format(name))
    x = time_stamps_1
    y = id_list_1
    x2 = time_stamps_2
    y2 = id_list_2
    # print(sum(time_stamps_1))
    # print(sum(time_stamps_2))
    fig, ax = plt.subplots()
    plt.title(name)
    plt.ylabel('Events')
    plt.xlabel('Time in (s)')

    ax.scatter(x, y,marker="|",color='r', label=name+'(arrival_inital)')

    ax.scatter(x2, y2,marker="|",color='g', label=name+'(arrival_final)')
    ax.legend()
    plt.savefig(res_dir+name+'.png',dpi=600)
    return


def main():
    args = parseArguments()
    with open('config.json') as json_config_file:
        data = json.load(json_config_file)
    print("Simulation process of {name} starts!\nInitializing with configs ...".format(**data))
    rng_seed = data["rng_seed"]
    main_scene = Scene(args.total_events,args.simulation_time,args.total_people,rng_seed)
    #  setting up input for vehicle_generate()
    initial_time_stamps, poisson = main_scene.poisson_generate_timestamps()
    initial_time_stamps_people, poisson = main_scene.poisson_generate_timestamps_people()

    np.random.seed(main_scene.rng_seed)
    print("time stamps initial \n")
    print(initial_time_stamps)
    num_trial = len(initial_time_stamps)
    car_type = np.zeros(shape=(num_trial,))
    which_lane = np.zeros(shape=(num_trial,))
    car_direction = np.zeros(shape=(num_trial,))
    car_id = np.arange(0, num_trial);
    for i in range(num_trial):
        car_type[i] = np.random.randint(3, size=1)
        which_lane[i] = np.random.randint(6, size=1)
        if(which_lane[i] == 4 or which_lane[i] == 3):
            car_direction[i] = np.random.randint(2, size=1)
        elif(which_lane[i] == 1 or which_lane[i] == 2):
            car_direction[i] = 0
        elif(which_lane[i] == 0 or which_lane[i] == 5):
            dir = np.random.randint(2, size = 1)
            print(dir)
            if (dir == 0):

                car_direction[i] = 0
            else:

                car_direction[i] = dir+1



    # setting up input for pedestrian zss
    initial_time_stamps_p = initial_time_stamps_people
    # print("car time stamp")
    # print(len(initial_time_stamps))
    # print(initial_time_stamps)
    # print("people time stamp")
    # print(len(initial_time_stamps_p))
    # print(initial_time_stamps_p)
    num_trial_p = len(initial_time_stamps_p)
    pedestrian_origin = np.zeros(shape=(num_trial_p,))
    pedestrian_destination = np.zeros(shape=(num_trial_p,))
    pedestrian_id = np.arange(0, num_trial_p)
    for i in range(num_trial_p):
        pedestrian_id[i] = i
        pedestrian_origin[i] = np.random.randint(low = 1, high = 4, size = 1)
        pedestrian_destination[i] = np.random.randint(low = 1, high = 4, size = 1)
        if (pedestrian_origin[i] == pedestrian_destination[i]):
            pedestrian_origin[i] = 5 - pedestrian_origin[i]

    # zss
    global_p_list = main_scene.pedestrian_generate(initial_time_stamps_p, pedestrian_id, pedestrian_origin,
                                                   pedestrian_destination)



    global_q = main_scene.vehicle_generate(initial_time_stamps, car_type, car_direction, which_lane,car_id)
    trafficLight = tl.TrafficLight([0,20], [20,23], [23,61])  # greenTime,yellowTime,redTime
    main_server = sr.server(trafficLight,global_q,global_p_list,args.simulation_time)
    updated_global_v_q,updated_global_p_q = main_server.run()



    # Create Plots
    output_plot = True
    all_lane_q = {}
    all_lane_q_final = []
    all_lane_q_id = {}
    all_lane_q_id_final = []
    for i in range(len(updated_global_v_q)):
        lane_q = []
        lane_q_id = []
        for j in range(len(updated_global_v_q[i])):
            lane_q.append(updated_global_v_q[i][j].timeStamp[-1])
            all_lane_q_final.append(updated_global_v_q[i][j].timeStamp[-1])
            lane_q_id.append(updated_global_v_q[i][j].ID)
            all_lane_q_id_final.append(updated_global_v_q[i][j].ID)
        all_lane_q[i] = lane_q
        all_lane_q_id[i] = lane_q_id

    init_all_lane_q = {}
    init_all_lane_q_final = []
    init_all_lane_q_id = {}
    init_all_lane_q_id_final = []
    for i in range(len(updated_global_v_q)):
        lane_q = []
        lane_q_id = []
        for j in range(len(updated_global_v_q[i])):
            lane_q.append(updated_global_v_q[i][j].timeStamp[0])
            init_all_lane_q_final.append(updated_global_v_q[i][j].timeStamp[0])
            lane_q_id.append(updated_global_v_q[i][j].ID)
            init_all_lane_q_id_final.append(updated_global_v_q[i][j].ID)
        init_all_lane_q[i] = lane_q
        init_all_lane_q_id[i] = lane_q_id

    if output_plot:
        save_timestamps_plot(initial_time_stamps, [i for i in range(len(initial_time_stamps))], 'Initial_Timestamps')
        save_poisson_hist_plot(poisson, 'Events_Poisson')
        save_timestamps_plot(all_lane_q[0], all_lane_q_id[0], 'Final_lane_0_Timestamps')
        save_timestamps_plot(all_lane_q[1], all_lane_q_id[1], 'Final_lane_1_Timestamps')
        save_timestamps_plot(all_lane_q[2], all_lane_q_id[2], 'Final_lane_2_Timestamps')
        save_timestamps_plot(all_lane_q[3], all_lane_q_id[3], 'Final_lane_3_Timestamps')
        save_timestamps_plot(all_lane_q[4], all_lane_q_id[4], 'Final_lane_4_Timestamps')
        save_timestamps_plot(all_lane_q[5], all_lane_q_id[5], 'Final_lane_5_Timestamps')
        save_timestamps_plot(all_lane_q_final, all_lane_q_id_final, 'Final_all_lanes_Timestamps')
        save_timestamps_plot(init_all_lane_q[0], init_all_lane_q_id[0], 'Initial_lane_0_Timestamps')
        save_timestamps_plot(init_all_lane_q[1], init_all_lane_q_id[1], 'Initial_lane_1_Timestamps')
        save_timestamps_plot(init_all_lane_q[2], init_all_lane_q_id[2], 'Initial_lane_2_Timestamps')
        save_timestamps_plot(init_all_lane_q[3], init_all_lane_q_id[3], 'Initial_lane_3_Timestamps')
        save_timestamps_plot(init_all_lane_q[4], init_all_lane_q_id[4], 'Initial_lane_4_Timestamps')
        save_timestamps_plot(init_all_lane_q[5], init_all_lane_q_id[5], 'Initial_lane_5_Timestamps')
        compare_timestamps_plot(initial_time_stamps, [i for i in range(len(initial_time_stamps))], all_lane_q_final,
                                all_lane_q_id_final, 'Comparison_all_lanes_Timestamps')
        compare_timestamps_plot(init_all_lane_q[0], init_all_lane_q_id[0], all_lane_q[0], all_lane_q_id[0],
                                'Comparison_lane_0_Timestamps')
        compare_timestamps_plot(init_all_lane_q[1], init_all_lane_q_id[1], all_lane_q[1], all_lane_q_id[1],
                                'Comparison_lane_1_Timestamps')
        compare_timestamps_plot(init_all_lane_q[2], init_all_lane_q_id[2], all_lane_q[2], all_lane_q_id[2],
                                'Comparison_lane_2_Timestamps')
        compare_timestamps_plot(init_all_lane_q[3], init_all_lane_q_id[3], all_lane_q[3], all_lane_q_id[3],
                                'Comparison_lane_3_Timestamps')
        compare_timestamps_plot(init_all_lane_q[4], init_all_lane_q_id[4], all_lane_q[4], all_lane_q_id[4],
                                'Comparison_lane_4_Timestamps')
        compare_timestamps_plot(init_all_lane_q[5], init_all_lane_q_id[5], all_lane_q[5], all_lane_q_id[5],
                                'Comparison_lane_5_Timestamps')

    # main_scene.pedestrain_generate()



if __name__ == "__main__":
    main() 
