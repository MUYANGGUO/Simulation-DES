class TrafficLight:
  def __init__(self, greenInterval,yellowInterval,redInterval):
    self.greenInterval = greenInterval
    self.yellowInterval = yellowInterval
    self.redInterval = redInterval
    self.cycle_time = 61;
    self.northLight = None;
    self.eastLight = None;
    self.westLight = None;
    self.pedsLight = None;

    return

  def setup(self):
      # end time for green yellow red
      self.northLight = TrafficLight([0,20], [20,20], [23,61])
      self.eastLight = TrafficLight([38,58],[58,58], [0,38])
      self.westLight = TrafficLight([38,58],[58,58], [0,38])
      self.pedsLight = TrafficLight([28,30],[0,23], [38,61])

