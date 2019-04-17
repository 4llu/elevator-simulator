from configuration import ELEVATOR_LOAD_TIME, FLOORS

class Elevator():
  def __init__(self):
    self.current_floor = 0
    self.target_floors = []
    self.direction = 0 # Options: -1 = Down, 0 = Idle, 1 = Up
    self.passangers = []
    self.wait_time = 0

  # ACT
  #####

  # Process actions (if any) for this tick
  def act(self, elevatorAI, people):

    # NOTE
    # Remove people that have been too long in the elevator
    removal_list = []
    for i, p in enumerate(self.passangers):
      if p.time_in_elevator > FLOORS * 2:
        removal_list.append(i)
        p.exit_elevator()

    removal_list.reverse()
    for i in removal_list:
      del self.passangers[i]

    ## Wait (Doors, opening/closing, etc.) ##
    if self.wait_time > 0:
      self.wait_time -= 1

    ## No orders currently ##
    elif len(self.target_floors) == 0:
      self.direction = 0

    ## Stop on target floor ##
    elif self.current_floor == self.target_floors[0]:
      # Add wait time
      self.wait_time = ELEVATOR_LOAD_TIME

      # Remove floor from targets
      self.target_floors.pop()

      # Let people out
      removal_list = []
      for i, passanger in enumerate(self.passangers):
        if passanger.target_floor == self.current_floor:
          passanger.exit_elevator()
          removal_list.append(i)

      # Remove people from passanger list
      removal_list.reverse()
      for i in removal_list:
        del self.passangers[i]

      direction = 1 if self.current_floor == 0 else -1

      # Get new people in
      for p in people:
        if p.waiting and p.get_direction() == direction:
          p.enter_elevator()
          self.passangers.append(p)
          self.go_to_floor(p.target_floor)

    ## Move a floor ##
    elif self.current_floor != self.target_floors[0]:
      self.current_floor += self.direction

    ## Error case ##
    else:
      print("Elevator confused")

  # UTILS
  #######

  def go_to_floor(self, floor):
    # Add to targets
    self.target_floors.append(floor)

    # Remove duplicates
    self.target_floors = list(set(self.target_floors))

    # Compute new direction if idle
    if len(self.target_floors) == 1:
      d = self.target_floors[0] - self.current_floor
      # If movement required
      if d != 0:
        self.direction = int(d / abs(d))
      # In case already on the right floor
      else:
        if self.direction == 0:
          self.direction = 1 if self.current_floor == 0 else -1

    # Reorder targets
    self.target_floors.sort()
    # Reverse if going down
    if self.direction < 0:
      self.target_floors.reverse()

    # print(self.target_floors)
    # print(self.current_floor, self.direction)
    if self.direction not in [-1, 1, 0]:
      print(self.direction, d)

  # Reset for a new day
  def reset(self):
    self.current_floor = 0
    self.target_floors = []
    self.direction = 0
    self.passangers = []
    self.wait_time = 0
