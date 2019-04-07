from datetime import datetime, timedelta
import random
import numpy as np

from configuration import *
from person import Person

def Simulation():
  def __init__(self):
    self.elevators = []
    self.people = []
    self.time = DAY_START_TIME
    self.day = 0

  def setup(self):
    # Create elevators
    self.elevators = [elevator() for i in range(ELEVATOR_NUM)]

    # Create people

    building_capacity = FLOORS * FLOOR_CAPACITY
    people_slots = random.sample(range(building_capacity),  building_capacity * BUILDING_FULLNESS)

    for ps in people_slots:
      home_floor = ps % FLOOR_CAPACITY
      entry_time = MEAN_ENTRY_TIME + timedelta(minutes=np.random.normal(0, 30))
      lunch_time = MEAN_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
      leave_time = MEAN_LEAVE_TIME + timedelta(minutes=np.random.normal(0, 30))

      self.people.append(Person(ps, "TODO", home_floor, entry_time, leave_time, lunch_time))

  def run(self, days):
    while self.day < days:
      # Move people
      for person in self.people:
        person.act(self.time)

      # Move elevators
      for elevator in self.elevators:
        elevator.act()

      # Move time
      self.time = self.time + timedelta(seconds=TICK_DURATION)

      # Check if the day is over
      if self.time.hour >= DAY_END_TIME.hour:
        # Move to next day
        self.time = DAY_START_TIME
        self.day += 1

        # Reset people
        for person in self.people:
          person.reset()

        # Reset elevators
        for elevator in self.elevators:
          elevator.reset()
