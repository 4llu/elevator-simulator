import random
import math
from datetime import datetime, timedelta
import numpy as np
import csv
from configuration import *

building_capacity = FLOORS * FLOOR_CAPACITY
people_slots = random.sample(range(building_capacity), math.ceil(building_capacity * BUILDING_FULLNESS))

data = []

# Datetime to string
def time(d):
  return d.strftime("%Y-%m-%d %H:%M:%S")

# Datetime (elevator entrance) to camera spotting time and to string
def spot_time(d):
  return time(d - timedelta(seconds=15))

for ps in people_slots:
  # Generate personal means
  home_floor = ps % FLOOR_CAPACITY
  mean_entry_time = MEAN_ENTRY_TIME + timedelta(minutes=np.random.normal(0, 30))
  mean_to_lunch_time = MEAN_TO_LUNCH_TIME + timedelta(minutes=np.random.normal(0, 30))
  mean_from_lunch_time = mean_to_lunch_time + timedelta(minutes=MEAN_LUNCH_TIME) + timedelta(minutes=np.random.normal(0, 5))
  mean_leave_time = MEAN_LEAVE_TIME + timedelta(minutes=np.random.normal(0, 30))

  for i in range(30):
    # Generate actual daily times
    entry_time = mean_entry_time + timedelta(minutes=np.random.normal(0, 5))
    to_lunch_time = mean_to_lunch_time + timedelta(minutes=np.random.normal(0, 5))
    from_lunch_time = mean_from_lunch_time + timedelta(minutes=np.random.normal(0, 5))
    leave_time = mean_leave_time + timedelta(minutes=np.random.normal(0, 5))

    # Insert event times
    # Data format:
    # (id, day, spot_time, elevator_time, current_floor, target_floor)

    # Entry time
    data.append((ps, i, spot_time(entry_time), time(entry_time), 0, home_floor))
    # To lunch time
    data.append((ps, i, spot_time(to_lunch_time), time(to_lunch_time), home_floor, 0))
    # From lunch time
    data.append((ps, i, spot_time(from_lunch_time), time(from_lunch_time), 0, home_floor))
    # Leave time
    data.append((ps, i, spot_time(leave_time), time(leave_time), home_floor, 0))

# Write data to file
with open("generated_data.csv", mode="w") as data_file:
  data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  for dp in data:
    data_writer.writerow(dp)
