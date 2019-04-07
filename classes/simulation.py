from datetime import datetime, timedelta
import random
import numpy as np

from configuration import *
from person import Person

def Simulation():
  def __init__(self):
    self.time = DAY_START_TIME
    self.elevators = []
    self.people = []

  def setup(self):
    # Create elevators
    self.elevators = [elevator() for i in range(ELEVATOR_NUM)]

    # Create people

    building_capacity = FLOORS * FLOOR_CAPACITY
    people_slots = random.sample(range(building_capacity),  building_capacity * BUILDING_FULLNESS)

    for p in people_slots:
      home_floor = p % FLOOR_CAPACITY
      entry_time = MEAN_ENTRY_TIME + timedelta(minutes=np.random.normal(0, 30))
      lunch_time = MEAN_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
      leave_time = MEAN_LEAVE_TIME + timedelta(minutes=np.random.normal(0, 30))
      
      self.people.append(Person(p, "TODO", home_floor, entry_time, leave_time, lunch_time))

  def run():
    # TODO
    pass
