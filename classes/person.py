from configuration import CAMERAS, TICKS_TO_ELEVATOR

# STATE ORDER

# 0 TO_WORK
# 1 WORKING
# 2 TO_LUNCH
# 3 LUNCH
# 4 FROM_LUNCH
# 5 WORKING_2
# 6 FROM_WORK


class Person:
  def __init__(self, id, home_floor, to_work_time, to_lunch_time, from_lunch_time, from_work_time):
    self.id = id
    self.home_floor = home_floor
    self.to_work_time = to_work_time
    self.to_lunch_time = to_lunch_time
    self.from_lunch_time = from_lunch_time
    self.from_work_time = from_work_time
    self.state = 0
    self.target_floor = -1
    self.current_floor = 0
    self.distance_to_elevator = 0
    self.waiting = False
    self.in_elevator = False
    self.waiting_ticks = 0

  # Process actions (if any) for this tick
  def act(self, time):
    # Log if waiting
    if self.waiting:
      self.waiting_ticks += 1

    # Do nothing if walking to elevator
    elif self.distance_to_elevator > 0:
      self.distance_to_elevator -= 1

      # Start waiting if arrived
      if self.distance_to_elevator == 0:
        self.waiting = True

    # TO_WORK
    elif self.state == 0 and time > self.to_work_time:
      self.target_floor = self.home_floor

      if CAMERAS:
        self.distance_to_elevator = TICKS_TO_ELEVATOR
      else:
        self.waiting = True

    # WORKING -> TO_LUNCH
    elif self.state == 1 and time > self.to_lunch_time:
      # FIXME Edit for naive solution
      self.state += 1
      self.target_floor = 0

      if CAMERAS:
        self.distance_to_elevator = TICKS_TO_ELEVATOR
      else:
        self.waiting = True

    # TO_LUNCH -> LUNCH (handled by elevator)

    # LUNCH -> FROM_LUNCH
    elif self.state == 3 and time > self.from_lunch_time:
      # FIXME Edit for naive solution
      self.state += 1
      self.target_floor = self.home_floor

      if CAMERAS:
        self.distance_to_elevator = TICKS_TO_ELEVATOR
      else:
        self.waiting = True

    # FROM_LUNCH -> WORKING_2 (Handled by elevator)

    # WORKING_2 -> FROM_WORK
    elif self.state == 5 and time > self.from_work_time:
      # FIXME Edit for naive solution
      self.state += 1
      self.target_floor = 0

      if CAMERAS:
        self.distance_to_elevator = TICKS_TO_ELEVATOR
      else:
        self.waiting = True

    # FROM_WORK (Out of building)
    else:
      pass

  def get_in_elevator(self):
    self.in_elevator = True
    self.waiting = False
  
  def get_out_of_elevator(self):
    self.in_elevator = False
    self.state += 1
    self.current_floor = self.target_floor
    self.target_floor = -1

  # Reset for a new day
  def reset(self):
    self.state = 0
