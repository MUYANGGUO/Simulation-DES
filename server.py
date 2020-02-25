import heapq
import json
import numpy as np
class server:

  def __init__(self, TrafficLight,global_v_list,global_p_list,simulation_duration):
      TrafficLight.setup()
      self.TrafficLight = TrafficLight
      self.global_v_list = global_v_list
      self.simulation_duration = int(simulation_duration*60*60)
      self.process_que = []
      self.is_available = [1,1,1,1,1,1]# [N1,N2,N3,N4,E1,W1]
      self.Now = [0,0,0,0,0,0]
      self.p = 1.00   #passing time
      self.pleft = 5.00   #leftpassing time
      self.pchangeline = 1.500
      self.changelinelikelihood = 1
      self.global_p_list = global_p_list
      self.pedstrian_passtime = 5
      self.greenlight = 0


      return

  def run(self):
      output_vehicle = []
      output_pedstrian = []
      updated_global_v_q = []
      updated_global_p_q = []
      for m in range(6):
          updated_global_v_q.append([])
          updated_global_p_q.append([])

      while(self.get_global_size(self.global_v_list) != 0): # run the vheicle simulation first
          cur_lane = self.pick_earliest(self.global_v_list)
          cur_car = self.global_v_list[cur_lane].pop(0)

          is_car_ahead = self.car_ahead(self.Now[cur_lane], self.is_available, cur_car)
          if(self.Now[cur_lane] == 0):
              self.Now[cur_lane] = cur_car.arrival_time

          waiteTime = self.update_wait_time(self.Now[cur_lane],cur_lane)

          if waiteTime > 0:
              self.greenlight = 0
              if self.is_available[cur_lane] == 0:
                  self.is_available[cur_lane] = 0
              else:
                  self.is_available[cur_lane] = 0
          else:
              self.greenlight = 1
              if self.is_available[cur_lane] == 1:
                  self.is_available[cur_lane] = 1
              else:
                  self.is_available[cur_lane] = 0



          if((not is_car_ahead) and (self.is_available[cur_lane] == 1)):   #no car ahead and green light
              if(cur_lane == 4 and cur_car.direction == 1):   #turn left
                 
                  if(cur_car.arrival_time + self.pleft > self.Now[5]):  #turn left OK
         
                      self.Now[cur_lane] = cur_car.arrival_time
                      cur_car.timeStamp.append(cur_car.arrival_time)
                      if(cur_car.leftwaitTime != 0):
                          cur_car.timeStamp.append(cur_car.leftwaitTime)
                      departure = cur_car.arrival_time + self.pleft
                      cur_car.timeStamp.append(departure)
                      self.Now[cur_lane] = departure
                  else:#turn left block
                      cur_car.timeStamp.append(cur_car.arrival_time)  # new add
                      self.Now[cur_lane] = self.Now[5]
                      cur_car.leftwaitTime = self.Now[cur_lane]
                      if (self.Now[cur_lane] + self.pleft > self.Now[5]):
                          departure = self.Now[cur_lane] + self.pleft
                          cur_car.timeStamp.append(departure)
                      else:
                          self.Now[cur_lane] = self.Now[cur_lane] + 10
              else:
                  self.Now[cur_lane] = cur_car.arrival_time
                  cur_car.timeStamp.append(cur_car.arrival_time)
                  departure = cur_car.arrival_time + self.p
                  cur_car.timeStamp.append(departure)
                  self.Now[cur_lane] = departure
          #elif(is_car_ahead and (self.is_available[cur_lane] == 1)):  #car ahead and green light
          elif(is_car_ahead and self.greenlight == 1 ):
              if(cur_lane <= 2 and cur_car.direction == 0 and self.changelinelikelihood == 1):
                  if(self.is_available[cur_lane + 1] == 1): #try to change lane if cur_lane + 1 is_available
               
                      self.Now[cur_lane + 1] = cur_car.arrival_time + self.pchangeline
                      cur_car.timeStamp.append(cur_car.arrival_time)
                      cur_car.timeStamp.append(self.Now[cur_lane + 1]) #waittime
                      departure = self.Now[cur_lane + 1] + self.p
                      cur_car.timeStamp.append(departure)
                      cur_car.laneHistoy.append(cur_lane + 1)
                  else:
                      cur_car.timeStamp.append(cur_car.arrival_time)
                      cur_car.timeStamp.append(self.Now[cur_lane])  # waittime
                      departure = self.Now[cur_lane] + self.p
                      cur_car.timeStamp.append(departure)
                      self.Now[cur_lane] = departure
              else:
                  cur_car.timeStamp.append(cur_car.arrival_time)
                  cur_car.timeStamp.append(self.Now[cur_lane])   #waittime
                  departure =  self.Now[cur_lane] + self.p
                  cur_car.timeStamp.append(departure)
                  self.Now[cur_lane] = departure
          elif((not is_car_ahead) and (self.is_available[cur_lane] == 0)):  #no car ahead and red light
              self.Now[cur_lane] = cur_car.arrival_time
              cur_car.timeStamp.append(cur_car.arrival_time)
              cur_car.timeStamp.append(cur_car.arrival_time + waiteTime)  #waitTime
              self.Now[cur_lane] = cur_car.arrival_time + waiteTime #new add
              departure = self.Now[cur_lane] + self.p
              cur_car.timeStamp.append(departure)
              self.Now[cur_lane] = departure
          else:       #a car ahead and red light
              #self.Now[cur_lane] = cur_car.arrival_time
              cur_car.timeStamp.append(cur_car.arrival_time)
              cur_car.timeStamp.append(cur_car.arrival_time + waiteTime)  #waitTime
              self.Now[cur_lane] = cur_car.arrival_time + waiteTime
              departure = self.Now[cur_lane] + 2 * self.p
              cur_car.timeStamp.append(departure)
              self.Now[cur_lane] = departure

          updated_global_v_q[int(cur_car.lane)].append(cur_car)
          if(cur_car.lane == 0 and  cur_car.direction == 2 ): # N1 right turn
              cur_car.lane = np.int64(6)
          elif(cur_car.lane == 3 and  cur_car.direction == 1):# N3 left turn
              cur_car.lane = np.int64(7)
          elif (cur_car.lane == 4 and cur_car.direction == 1):# E1 left turn
              cur_car.lane = np.int64(8)
          elif (cur_car.lane == 5 and cur_car.direction == 2):  # W1 right turn
              cur_car.lane = np.int64(9)

          if(len(cur_car.timeStamp) >2 and cur_car.timeStamp[0] == cur_car.timeStamp[1]):
              cur_car.timeStamp.pop(1)

          #Add coordinate
          #if(cur_car.direction == 6 and cur_car.direction == 7 and cur_car.direction == 8 and cur_car.direction == 9):
          coordinates = [];
          add_time = 2
          if (len(cur_car.timeStamp) == 2):

              if (cur_car.lane == 0):  #0
                  # coordinates = [[-84.388820, 33.777044],[-84.388825, 33.776667]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388820, 33.777044],[-84.388820,33.776930], [-84.388825, 33.776667]]
              elif (cur_car.lane == 1):  #1
                  # coordinates = [[-84.388800, 33.777044],[-84.388805, 33.776667]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388800, 33.777044],[-84.388800,33.776930], [-84.388805, 33.776667]]
              elif (cur_car.lane == 2):  #2
                  # coordinates = [[-84.388780, 33.777044],[-84.388785, 33.776667]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388780, 33.777044],[-84.388780,33.776930],[-84.388785, 33.776667]]
              elif (cur_car.lane == 3):  #3
                  # coordinates = [[-84.388760, 33.777044],[-84.388765, 33.776667]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388760, 33.777044],[-84.388760,33.776930],[-84.388765, 33.776667]]
              elif (cur_car.lane == 4):  #4
                  # coordinates = [[-84.388520, 33.776857],[-84.389000, 33.776866]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388520, 33.776857],[-84.388690, 33.776857], [-84.389000, 33.776866]]
              elif (cur_car.lane == 5):  #5
                  # coordinates = [[-84.389000, 33.776834],[-84.388520, 33.776824]]
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.389000, 33.776834],[-84.388895, 33.776834], [-84.388520, 33.776824]]
              elif (cur_car.lane == 6):
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1])/2)
                  coordinates = [[-84.388820, 33.777044], [-84.388820, 33.776866], [-84.389000, 33.776866]];
              elif(cur_car.lane == 7):
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388760, 33.777044],[-84.388760, 33.776824],[-84.388520, 33.776824]];
              elif (cur_car.lane == 8):
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.388520, 33.776857],[-84.388765,33.776857], [-84.388765, 33.776667]];
              elif (cur_car.lane == 9):
                  cur_car.timeStamp.insert(1, (cur_car.timeStamp[0] + cur_car.timeStamp[1]) / 2)
                  coordinates = [[-84.389000, 33.776834],[-84.388825,33.776830],[-84.388825, 33.776667]];
          else:
              if (cur_car.lane == 0):
                  if(len(cur_car.laneHistoy) > 1):
                      coordinates = [[-84.388820, 33.777044],[-84.388800,33.776930],[-84.388805, 33.776667]]
                  else:
                      coordinates = [[-84.388820, 33.777044],[-84.388820,33.776930],[-84.388825, 33.776667]]
              elif (cur_car.lane == 1):
                  if (len(cur_car.laneHistoy) > 1):
                      coordinates =[[-84.388800, 33.777044],[-84.388780,33.776930],[-84.388785, 33.776667]]
                  else:
                      coordinates = [[-84.388800, 33.777044],[-84.388800,33.776930],[-84.388805, 33.776667]]
              elif (cur_car.lane == 2):
                  if (len(cur_car.laneHistoy) > 1):
                      coordinates =[[-84.388780, 33.777044],[-84.388760,33.776930],[-84.388765, 33.776667]]
                  else:
                      coordinates = [[-84.388780, 33.777044],[-84.388780,33.776930],[-84.388785, 33.776667]]
              elif (cur_car.lane == 3):
                  coordinates = [[-84.388760, 33.777044],[-84.388760,33.776930],[-84.388765, 33.776667]]
              elif (cur_car.lane == 4):
                  coordinates = [[-84.388520, 33.776857],[-84.388690, 33.776857],[-84.389000, 33.776866]]
              elif (cur_car.lane == 5):
                  coordinates = [[-84.389000, 33.776834],[-84.388895, 33.776834],[-84.388520, 33.776824]]
              elif (cur_car.lane == 6):
                  coordinates = [[-84.388820, 33.777044], [-84.388820, 33.776866], [-84.389000, 33.776866]]
              elif(cur_car.lane == 7):
                  coordinates = [[-84.388760, 33.777044],[-84.388760, 33.776824],[-84.388520, 33.776824]]
              elif (cur_car.lane == 8):
                  coordinates = [[-84.388520, 33.776857],[-84.388765,33.776857], [-84.388765, 33.776667]]
              elif (cur_car.lane == 9):
                  coordinates = [[-84.389000, 33.776834],[-84.388825,33.776830],[-84.388825, 33.776667]]


          cur_car_data = {'id': cur_car.ID.tolist(),'timestamps':(cur_car.timeStamp),'lane':cur_car.lane.tolist(),'lane_history':cur_car.laneHistoy,
                          'path':coordinates}
          output_vehicle.append(cur_car_data)
        #   print(cur_car)
        #   print(str(cur_car.timeStamp[:]) + " Time stamp \n" )

      # run the pedstrian simulation
      output_pedstrian = []
      while (len(self.global_p_list) != 0):  #run the pedstrian simulation
          cur_ped = self.global_p_list.pop(0)
          pedWaitTime = self.update_wait_time(cur_ped.arrival_time,-1)
          cur_ped.timeStamp.append(cur_ped.arrival_time)
          if(pedWaitTime > 0):
              cur_ped.timeStamp.append(cur_ped.arrival_time + pedWaitTime)
          cur_ped.timeStamp.append(cur_ped.arrival_time + pedWaitTime + self.pedstrian_passtime)

          # Pedstrian_Position
          # [1,2,3,4]
          ped_postion =[[-84.388896,33.776921],[-84.388896,33.776779],[-84.388703,33.776779],[-84.388703,33.776923]]
          ped_postion_wait =[[-84.388896 - 0.000040 ,33.776921],[-84.388896 - 0.000040,33.776779],[-84.388703+ 0.000040,33.776779],[-84.388703+ 0.000040,33.776923]]

          if(len(cur_ped.timeStamp) ==2):
              cur_ped.timeStamp.insert(1,(cur_ped.timeStamp[0] + cur_ped.timeStamp[1]) / 4)

          coordinates = [ped_postion_wait[int(cur_ped.origin)-1],ped_postion[int(cur_ped.origin)-1],ped_postion[int(cur_ped.destination)-1]];
          cur_ped_data = {'id': cur_ped.ID.tolist(), 'timestamps': (cur_ped.timeStamp), 'lane': cur_ped.lane,
                          'path': coordinates}


          output_vehicle.append(cur_ped_data)
          updated_global_p_q[int(cur_ped.origin)].append(cur_ped)
        #   print(cur_ped)
          # cur_ped_data = {'id': int(cur_ped.ID),'timestamps': (cur_ped.timeStamp), 'origin': int(cur_ped.origin), 'destination': int(cur_ped.destination)}
          # output_vehicle.append(cur_ped_data)


      with open('./Visualization/test.json', 'w') as fout:
          json.dump(output_vehicle, fout)
      return updated_global_v_q,updated_global_p_q


  def update_wait_time(self, arrival_time,lane):
      cycle_time = self.TrafficLight.cycle_time
      # North Lane
      if(0<= lane <= 3):
          curlight = self.TrafficLight.northLight
          mod_time = arrival_time % cycle_time
          return self.calculate_wait_time(curlight,mod_time)
      # East Lane
      elif(lane == 4):
          curlight = self.TrafficLight.eastLight
          mod_time = arrival_time % cycle_time
          return self.calculate_wait_time(curlight,mod_time)
      #West Lane
      elif(lane == 5):
          curlight = self.TrafficLight.westLight
          mod_time = arrival_time % cycle_time
          return self.calculate_wait_time(curlight,mod_time)
      # Pedstrian Light
      else:
          curlight = self.TrafficLight.pedsLight
          mod_time = arrival_time % cycle_time
          return self.calculate_wait_time_ped(curlight, mod_time)

  def calculate_wait_time(self, tl, mod_time):
     if (tl.greenInterval[0]<=mod_time and mod_time <tl.greenInterval[1]):
         return 0
     elif (tl.yellowInterval[0]<=mod_time and mod_time <tl.yellowInterval[1]):
         return 0
     else:
         return tl.redInterval[1] - mod_time

  def calculate_wait_time_ped(self, tl, mod_time):
     if (tl.greenInterval[0]<=mod_time and mod_time <tl.greenInterval[1]):
         return 0
     elif (tl.greenInterval[1]<mod_time):
         return mod_time -tl.greenInterval[1] +tl.yellowInterval[1]
     elif (mod_time < tl.greenInterval[0]):
         return tl.greenInterval[0] - mod_time

  #update local single lane wait time
  def update_singlelane_waittime(self, local_q_list, lane, cur_second):

      local_q_list[0].waiteTime = self.update_wait_time(cur_second,lane)

      if(len(local_q_list) > 1):
          for i in range(1,len(local_q_list)):
              if(local_q_list[i-1].arrival_time < local_q_list[i].arrival_time < local_q_list[i-1].arrival_time + local_q_list[i-1].waiteTime):
                  self.process_que[i].waiteTime = local_q_list[i-1].arrival_time + local_q_list[i-1].waiteTime - local_q_list[i].arrival_time


  def get_global_size(self,q_arr):
      size = 0;
      for i in range(len(q_arr)):
          size = size+ len(q_arr[i])
      return size

  def pick_earliest(self, list):
      tmp = 2147483647
      tag = 0
      for i in range(len(list)):
          if(len(list[i]) > 0):
              if(list[i][0].arrival_time < tmp):
                  tmp = list[i][0].arrival_time
                  tag = i
      return tag

  def car_ahead(self, local_now,  is_available, car):
      lane = int(car.lane)
      if(car.arrival_time < local_now):
          self.is_available[lane] = 0
          return True;
      else:
          self.is_available[lane] = 1
          return False;




