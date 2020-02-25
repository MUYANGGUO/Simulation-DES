import numpy as np
import math as math
import heapq

class Vehicle:
  def __init__(self, arrival_time,type,direction,lane,ID):
    self.ID = ID
    self.direction = direction
    self.lane = lane
    self.type = type
    self.arrival_time = arrival_time
    self.waiteTime = 0
    self.leftwaitTime = 0
    self.timeStamp = []
    self.laneHistoy = [lane]
  def __repr__(self):
    return "Vehicle ID : " + str(self.ID) + " "  + ", Direction: " + str(self.direction) +" cur Lane :" + str(self.lane) +" New Lane :" + str(self.laneHistoy[-1])
  def __lt__(self, other):
    return self.arrival_time > other.arrival_time


