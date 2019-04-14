from datetime import datetime, timedelta
import random
import math
import numpy as np
from functools import reduce

from configuration import *
from classes.person import Person
from classes.elevator import Elevator
from classes.elevatorAI import ElevatorAI
from classes.logger import Logger

class Simulation():
  def __init__(self):
    self.elevators = [Elevator() for i in range(ELEVATOR_NUM)]
    self.elevatorAI = ElevatorAI(self.elevators)
    self.people = []
    self.time = DAY_START_TIME
    self.day = 0
    self.logger = Logger()

  # Create the people for the simulation
  def populate(self):
    # Create people
    building_capacity = (FLOORS - 1) * FLOOR_CAPACITY # -1 because floor 0 is not a valid home floor
    people_slots = random.sample(range(building_capacity),  math.ceil(building_capacity * BUILDING_FULLNESS))

    for ps in people_slots:
      home_floor = math.floor(ps/FLOOR_CAPACITY) + 1 # +1 because 0 is not a valid home floor
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
        elevator.act(self.elevatorAI.going_down[elevator.current_floor], self.elevatorAI.going_up[elevator.current_floor], self.elevatorAI)

      # Move time
      self.time = self.time + timedelta(seconds=TICK_DURATION)

      # Check if the day is over
      if self.time.hour >= DAY_END_TIME.hour:
        # Move to next day
        self.day += 1
        self.time = DAY_START_TIME + timedelta(days=self.day)

        # Reset people
        for person in self.people:
          person.reset()

        # Reset elevators
        for elevator in self.elevators:
          elevator.reset()

      # At the end of each cycle
      self.logger.log_people_movement(self.time, self.people)

    print(self.logger.get_total_waiting_time())
    print(self.logger.get_total_elevator_time())
    self.logger.save_to_file()
