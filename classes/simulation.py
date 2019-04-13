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
    self.time = DAY_START_TIME
    self.day = 0

  # Create the people for the simulation
  def populate(self):
    # Create people
    building_capacity = FLOORS * FLOOR_CAPACITY
    people_slots = random.sample(range(building_capacity),  math.ceil(building_capacity * BUILDING_FULLNESS))

    for ps in people_slots:
      home_floor = ps % FLOOR_CAPACITY
      entry_time = MEAN_ENTRY_TIME + timedelta(minutes=np.random.normal(0, 30))
      to_lunch_time = MEAN_TO_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
      from_lunch_time = to_lunch_time + timedelta(minutes=MEAN_LUNCH_TIME) + timedelta(minutes=np.random.normal(0, 5))
      leave_time = MEAN_LEAVE_TIME + timedelta(minutes=np.random.normal(0, 30))

      self.people.append(Person(ps, home_floor, entry_time, to_lunch_time, from_lunch_time, leave_time))

  def run(self, days):
    # Main loop
    while self.day < days:

      # Move people
      for person in self.people:
        person.act(self.time)

        # Check if spotted by camera
        if person.distance_to_elevator == TIME_TO_ELEVATOR:
          # Call elevator (prediction)
          self.elevatorAI.call_elevator_prediction(person.current_floor, person.target_floor)

        # Check if waiting for elevator
        if person.waiting and not person.elevator_called:
          # Call elevator
          direction = -1 if person.target_floor - person.current_floor > 0 else -1
          self.elevatorAI.call_elevator(person, person.current_floor, direction)
          person.elevator_called = True

      # Update elevator orders
      self.elevatorAI.act()

      # Move elevators
      for elevator in self.elevators:
        elevator.act(self.elevatorAI.going_down[elevator.current_floor], self.elevatorAI.going_up[elevator.current_floor])

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
