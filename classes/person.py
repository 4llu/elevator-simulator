class Person:
  def __init__(self, id, face, home_floor, entry_time, leave_time, lunch_time):
    self.id = id
    self.face = face
    self.home_floor = home_floor
    self.entry_time = entry_time # Mean
    self.leave_time = leave_time # Mean
    self.lunch_time = lunch_time # Mean
    self.in_elevator = False

  def act(self):
    # TODO
    pass
