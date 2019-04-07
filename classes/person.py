# States
TO_WORK = "to_work"
WORKING = "working"
FROM_WORK = "from_work"
TO_EAT = "to_eat"
EATING = "eating"
FROM_EATING = "from_eating"
WAITING = "waiting"
IN_ELEVATOR = "in_elevator"

class Person:
  def __init__(self, id, face, home_floor, entry_time, lunch_time, leave_time):
    self.id = id
    self.face = face
    self.home_floor = home_floor
    self.entry_time = entry_time # Mean
    self.lunch_time = lunch_time # Mean
    self.leave_time = leave_time # Mean
    self.status = TO_WORK

  # Process actions (if any) for this tick
  def act(self, time):
    # TODO
    pass

  # Reset for a new day
  def reset(self):
    self.status = TO_WORK
