from datetime import datetime, timedelta
import random
import math
import numpy as np

from configuration import *
from classes.person import Person
from classes.elevator import Elevator
from classes.elevatorAI import ElevatorAI

class Simulation():
  def __init__(self):
    self.elevators = [Elevator() for i in range(ELEVATOR_NUM)]
    self.elevatorAI = ElevatorAI(self.elevators)
    self.people = []
    self.walking_list = [[] for i in range(FLOORS)]
    self.waiting_list = [[] for i in range(FLOORS)]
    self.time = DAY_START_TIME
    self.day = 0

  def populate(self):
    # Create people
    building_capacity = FLOORS * FLOOR_CAPACITY
    people_slots = random.sample(range(building_capacity),  math.ceil(building_capacity * BUILDING_FULLNESS))

    for ps in people_slots:
      home_floor = ps % FLOOR_CAPACITY
      entry_time = MEAN_ENTRY_TIME + timedelta(minutes=np.random.normal(0, 30))
      to_lunch_time = MEAN_TO_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
      from_lunch_time = MEAN_FROM_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
      leave_time = MEAN_LEAVE_TIME + timedelta(minutes=np.random.normal(0, 30))

      self.people.append(Person(ps, home_floor, entry_time, to_lunch_time, from_lunch_time, leave_time))

  def run(self, days):
    while self.day < days:
      # Move people
      for person in self.people:
        person.act(self.time)

        # Check if walking to elevator
        if person.distance_to_elevator > 0 and person not in self.walking_list:
          direction = "UP" if person.target_floor - person.current_floor > 0 else "DOWN" # FIXME Make into function

          # Add to queue
          self.walking_list[person.current_floor].append((person, direction))
          # Call elevator (by prediction)
          self.elevatorAI.call_elevator_prediction(person.current_floor, direction)

        # Check if waiting for elevator
        if person.waiting and person not in self.waiting_list:
          # Remove from walking list
          for i, p in enumerate(self.walking_list[person.current_floor]):
            if p.id == person.id:
              del self.walking_list[person.current_floor][i]

          direction = "UP" if person.target_floor - person.current_floor > 0 else "DOWN"

          # Add to queue
          self.waiting_list[person.current_floor].append((person, direction))
          # Call elevator
          self.elevatorAI.call_elevator(person.current_floor, direction)

      # Move elevators
      self.elevatorAI.act(self.waiting_list, self.walking_list)

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
