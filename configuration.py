from datetime import datetime

# Building
FLOORS = 20
FLOOR_CAPACITY = 24
BUILDING_FULLNESS = 0.8

# Elevators
ELEVATOR_AI = "BASIC" # Other options [MEDIUM, ADVANCED]
CAMERAS = False
ELEVATOR_NUM = 3
ELEVATOR_CAPACITY = 8
TIME_TO_ELEVATOR = 8 # Ticks it takes to walk to the elevator from the camera in ticks
ELEVATOR_LOAD_TIME = 4 # Ticks it takes for people to get in and out of the elevator

# People
MEAN_ENTRY_TIME = datetime(2019, 1, 1, 8)
MEAN_TO_LUNCH_TIME = datetime(2019, 1, 1, 11, 30)
MEAN_LUNCH_TIME = 45
MEAN_LEAVE_TIME = datetime(2019, 1, 1, 17)

# Time
DAY_START_TIME = datetime(2019, 1, 1, 6)
DAY_END_TIME = datetime(2019, 1, 1, 21)
RUN_DAYS = 3
TICK_DURATION = 2 # In seconds
