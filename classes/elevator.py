from configuration import ELEVATOR_CAPACITY

class elevator():
  def __init__(self):
    self.capacity = ELEVATOR_CAPACITY
    self.current_floor = 1
    self.passangers = []

  def act(self):
    # TODO
    pass