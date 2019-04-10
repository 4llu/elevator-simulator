from datetime import datetime

# Building
FLOORS = 30
FLOOR_CAPACITY = 40
BUILDING_FULLNESS = 0.8

# Elevators
ELEVATOR_AI = "BASIC" # Other options [MEDIUM, ADVANCED]
CAMERAS = False
ELEVATOR_NUM = 4
ELEVATOR_CAPACITY = 8
TICKS_TO_ELEVATOR = 8 # Time it takes to walk to the elevator from the camera in ticks

# People
MEAN_ENTRY_TIME = datetime(2019, 4, 7, 8)
MEAN_TO_LUNCH_TIME = datetime(2019, 4, 7, 11, 30)
MEAN_FROM_LUNCH_TIME = datetime(2019, 4, 7, 12, 30)
MEAN_LEAVE_TIME = datetime(2019, 4, 7, 17)

# Time
DAY_START_TIME = datetime(2019, 4, 6)
DAY_END_TIME = datetime(2019, 4, 21)
RUN_DAYS = 3
TICK_DURATION = 2 # In seconds
