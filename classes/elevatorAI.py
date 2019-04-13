from configuration import ELEVATOR_AI, FLOORS

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
    # Add to lists if not already called
    if not (floor, direction) in self.queue:
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

  def basicAI(self):
    # Free elevators
    free_elevators = []
    for elevator in self.elevators:
      if elevator.direction == 0:
        free_elevators.append(elevator)
    # Sort lowest first
    free_elevators = sorted(free_elevators, key=lambda e: e.current_floor)

    # Elevators going down
    up_elevators = []
    for elevator in self.elevators:
      if elevator.direction == 1:
        up_elevators.append(elevator)
    # Sort highest first
    up_elevators = sorted(up_elevators, key=lambda e : -e.current_floor)

    # Elevators going down
    down_elevators = []
    for elevator in self.elevators:
      if elevator.direction == -1:
        down_elevators.append(elevator)
    # Sort lowest first
    down_elevators = sorted(down_elevators, key=lambda e : e.current_floor)

    # Separate calls per direction
    up_calls = list(filter(lambda c: c[1] == 1, self.queue)) # NOTE Technically uselless, as only up calls come from floor 0
    down_calls = list(filter(lambda c: c[1] == -1, self.queue))
    # Sort lowest first
    up_calls = sorted(up_calls, key=lambda c : c[0]) # NOTE Technically uselless, as only up calls come from floor 0
    down_calls = sorted(down_calls, key=lambda c : c[0])

    # Assign up going elevators (to free elevators)
    # NOTE Technically overkill, as only up calls come from floor 0
    if len(free_elevators) > 0:
      for c in up_calls:
        free_elevators[0].go_to_floor(c[0])
        # Remove call from call queue
        self.queue.remove(c)

      # Remove elevator from free elevators if a call was added to it
      if len(up_calls) > 1:
        del free_elevators[0]

    # Assign down going elevators (to already down going elevators)
    if len(down_elevators) > 0:
      # Assign all possible calls to highest down going elevator
      i = 0
      while i < len(down_calls):
        # Check that elevator is above the call floor
        if down_elevators[-1].current_floor > down_calls[i][0]:
          # Add target floor
          down_elevators[-1].go_to_floor(down_calls[i][0])
          # Remove from calls
          self.queue.remove(down_calls[i])
          del down_calls[i]
        else:
          i += 1

    # If calls left, add them to the (possible) free elevator
    if len(down_calls) > 0 and len(free_elevators) > 0:
      for c in down_calls:
        free_elevators[0].go_to_floor(c[0])

    # Any calls left carry on to the next tick

  def mediumAI(self):
    pass

  def advancedAI(self):
    pass
