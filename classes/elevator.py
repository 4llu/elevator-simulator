from configuration import ELEVATOR_CAPACITY

class elevator():
  def __init__(self):
    self.capacity = ELEVATOR_CAPACITY
    self.current_floor = 0
    self.passangers = []

  # Process actions (if any) for this tick
  def act(self):
    # TODO
    pass

  # Reset for a new day
  def reset(self):
    self.current_floor = 0
    self.passangers = []
