from configuration import ELEVATOR_AI, ELEVATOR_CAPACITY, FLOORS

class ElevatorAI():
  def __init__(self, elevators):
    self.elevators = elevators
    self.queue = [] # (floor, direction)
    self.prediction_queue = [] # (current_floor, target_floor)
    self.going_up = [[] for i in range(FLOORS)]
    self.going_down = [[] for i in range(FLOORS)]

  def act(self):
    if ELEVATOR_AI == "BASIC":
      self.basicAI()
    elif ELEVATOR_AI == "MEDIUM":
      self.mediumAI()
    elif ELEVATOR_AI == "ADVANCED":
      self.advancedAI()
    else:
      print("Elevator AI not chosen properly!")
      print("ELEVATOR_AI: " + ELEVATOR_AI)

  # Basic elevator call
  def call_elevator(self, person, floor, direction):
    # Call list
    self.queue.append((floor, direction))
    # People list
    if direction > 0:
      self.going_up[floor].append(person)
    else:
      self.going_down[floor].append(person)

  # Predictive elevator call
  def call_elevator_prediction(self, floor, target_floor):
    self.prediction_queue.append((floor, target_floor))

  # Remove people that have entered elevators from waiting lists (called after elevators take people in)
  def clear_waiting_lists(self):
    # Going up
    removal_list = []
    for f in range(self.going_up):
      for p in range(self.going_up[f]):
        if self.going_up[f][p].in_elevator:
          removal_list.append((f, p))

    for (f, p) in removal_list.reverse():
      del self.going_up[f][p]

    # Going down
    removal_list = []
    for f in range(self.going_down):
      for p in range(self.going_down[f]):
        if self.going_down[f][p].in_elevator:
          removal_list.append((f, p))

    for (f, p) in removal_list.reverse():
      del self.going_down[f][p]

  def get_free_elevators(self):
    free_elevators = []
    for elevator in self.elevators:
        if elevator.direction == 0:
          free_elevators.append(elevator)
    # Return with lowest first
    return sorted(free_elevators, key=lambda e: e.current_floor)

  def get_up_elevators(self):
    up_elevators = []
    for elevator in self.elevators:
      if elevator.direction == 1:
        up_elevators.append(elevator)
    # Sort highest first and return
    return sorted(up_elevators, key=lambda e: -e.current_floor)

  def get_down_elevators(self):
    down_elevators = []
    for elevator in self.elevators:
      if elevator.direction == -1:
        down_elevators.append(elevator)
    # Sort lowest first and return
    return sorted(down_elevators, key=lambda e : e.current_floor)

  def get_up_calls(self):
    # Separate calls per direction
    up_calls = list(filter(lambda c: c[1] == 1, self.queue))
    # Sort lowest first
    return sorted(up_calls, key=lambda c : c[0]) # NOTE Technically uselless, as only up calls come from floor 0

  def get_down_calls(self):
    # Separate calls per direction
    down_calls = list(filter(lambda c: c[1] == -1, self.queue))
    # Sort lowest first
    return sorted(down_calls, key=lambda c : c[0])


  def basicAI(self):
    # Elevator list
    free_elevators = self.get_free_elevators()
    # up_elevators = self.get_up_elevators() # NOTE Technically not necessary with current setup
    down_elevators = self.get_down_elevators()

    # Call lists
    up_calls = self.get_up_calls()
    down_calls = self.get_down_calls()


    # Assign up going elevators (to free elevators)
    # NOTE Technically overkill, as only up calls come from floor 0
    while len(free_elevators) > 0 and len(up_calls) > 0:
      i = 0 # Call index (to keep track of elevator capacity)

      while i < ELEVATOR_CAPACITY and len(up_calls) > 0:
        # Add target floor
        free_elevators[0].go_to_floor(up_calls[0][0])
        # Remove from lists
        del up_calls[0]
        self.queue.remove(up_calls[0])

        i += 1

      # Elevator no longer free
      del free_elevators[0]

    # Assign down going elevators (to already down going elevators)
    if len(down_elevators) > 0 and len(down_calls) > 0:
      i = 0 # Call index (to keep tack of elevator capacity)
      # Assign all possible calls to highest down going elevator
      while i < ELEVATOR_CAPACITY and len(down_calls) > 0:
        # Check that elevator is above the call floor
        if down_elevators[-1].current_floor > down_calls[0][0]:
          # Add target floor
          down_elevators[-1].go_to_floor(down_calls[0][0])
          # Remove from calls
          self.queue.remove(down_calls[0])
          del down_calls[0]

          i += 1

      # Elevator full
      del down_elevators[-1]

    # If calls left, add them to the (possible) free elevator
    while len(down_calls) > 0 and len(free_elevators) > 0:
      i = 0 # Call index (to keep track of elevator capacity)
      while i < ELEVATOR_CAPACITY and len(down_calls) > 0:
        # Add target floor
        free_elevators[0].go_to_floor(down_calls[0][0])
        # Remove from calls
        self.queue.remove(down_calls[0])
        del down_calls[0]

        i += 1

      # Elevator full
      del free_elevators[0]

    # Any calls left carry on to the next tick

  def mediumAI(self):
    # Do everything the same as in basic AI
    self.basicAI()

    free_elevators = self.get_free_elevators()

    # Send free elevators to prediction queue targets
    while len(free_elevators) > 0 and len(self.prediction_queue) > 0:
      # Send elevator
      free_elevators[0].go_to_floor(self.prediction_queue[0])

      del free_elevators[0]
      del self.prediction_queue[0]

  def advancedAI(self):
    pass
