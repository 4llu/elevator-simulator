from configuration import ELEVATOR_AI, TIME_TO_ELEVATOR, FLOORS
from datetime import timedelta

# STATE ORDER

# 0 TO_WORK
# 1 WORKING
# 2 TO_LUNCH
# 3 LUNCH
# 4 FROM_LUNCH
# 5 WORKING_2
# 6 FROM_WORK
# 7 AT_HOME


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
    self.elevator_called = False
    self.time_waiting = 0
    self.time_in_elevator = 0

  # UTILS
  ########

  def get_direction(self):
    return 1 if self.current_floor == 0 else -1

  # ACT
  #####

  # Process actions (if any) for this tick
  def act(self, time):
    # Do nothing if in elevator
    if self.waiting:
      pass

    # Log if in elevator
    if self.in_elevator:
      self.time_in_elevator += 1

    # Log if waiting
    if self.waiting:
      self.time_waiting += 1

    # NOTE
    # Remove from waiting if stuck waiting
    if self.time_waiting > FLOORS * 2:
      self.enter_elevator()
      self.exit_elevator()

    # Do nothing if walking to elevator
    elif self.distance_to_elevator > 0:
      self.distance_to_elevator -= 1

      # Start waiting if arrived
      if self.distance_to_elevator == 0:
        self.waiting = True

    # TO_WORK
    elif self.state == 0 and time > self.to_work_time and not (self.waiting or self.in_elevator):
      self.target_floor = self.home_floor

      if ELEVATOR_AI == "MEDIUM":
        self.distance_to_elevator = TIME_TO_ELEVATOR
      else:
        self.waiting = True

    # WORKING -> TO_LUNCH
    elif self.state == 1 and time > self.to_lunch_time and not (self.waiting or self.in_elevator):
      self.state += 1
      self.target_floor = 0

      if ELEVATOR_AI == "MEDIUM":
        self.distance_to_elevator = TIME_TO_ELEVATOR
      else:
        self.waiting = True

    # TO_LUNCH -> LUNCH (handled by elevator)

    # LUNCH -> FROM_LUNCH
    elif self.state == 3 and time > self.from_lunch_time and not (self.waiting or self.in_elevator):
      self.state += 1
      self.target_floor = self.home_floor

      if ELEVATOR_AI == "MEDIUM":
        self.distance_to_elevator = TIME_TO_ELEVATOR
      else:
        self.waiting = True

    # FROM_LUNCH -> WORKING_2 (Handled by elevator)

    # WORKING_2 -> FROM_WORK
    elif self.state == 5 and time > self.from_work_time and not (self.waiting or self.in_elevator):
      self.state += 1
      self.target_floor = 0

      if ELEVATOR_AI == "MEDIUM":
        self.distance_to_elevator = TIME_TO_ELEVATOR
      else:
        self.waiting = True

    # AT_HOME (Out of building)
    elif self.state == 7:
      pass

    # Error case
    elif self.state not in [0, 1, 2, 3, 4, 5, 6, 7]:
      print("Person state not set correctly!")
      print("Current state: " + str(self.state))

  # ELEVATOR INTERACTIONS
  #######################

  def enter_elevator(self):
    self.in_elevator = True
    self.waiting = False
    self.elevator_called = False
  
  def exit_elevator(self):
    self.in_elevator = False
    self.state += 1
    self.current_floor = self.target_floor
    self.target_floor = -1
    self.time_waiting = 0
    self.time_in_elevator = 0

  # Reset for a new day
  def next_day(self):
    # Reset values
    self.state = 0
    self.target_floor = -1
    self.current_floor = 0
    self.distance_to_elevator = 0
    self.waiting = False
    self.in_elevator = False
    self.elevator_called = False

    # Move days forwards
    self.to_work_time += timedelta(days=1)
    self.to_lunch_time += timedelta(days=1)
    self.from_lunch_time += timedelta(days=1)
    self.from_work_time += timedelta(days=1)
