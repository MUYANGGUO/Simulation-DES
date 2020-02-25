import numpy as np
import math as math
import heapq

class Pedestrian:
  def __init__(self,arrival_time,ID,origin,destination):
    self.ID = ID*(-1)
    self.arrival_time = arrival_time
    self.origin = origin
    self.destination = destination
    self.wait_time = 0
    self.timeStamp = []
    self.lane = 10

  def __repr__(self):
    return "Pedestrian ID : " + str(self.ID) + " " + "timeStamp: " +str(self.timeStamp) + ", From: " + str(self.origin) + ", To: " + str(self.destination)
  def __lt__(self, other):
    return self.arrival_time < other.arrival_time
