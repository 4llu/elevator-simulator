from configuration import ELEVATOR_AI

class ElevatorAI():
  def __init__(self, elevators):
    self.elevators = elevators
    self.queue = []
    self.prediction_queue = []

  def act(self, waiting_list, walking_list):
    if ELEVATOR_AI == "BASIC":
      self.basicAI(waiting_list)
      pass
    elif ELEVATOR_AI == "MEDIUM":
      pass
    elif ELEVATOR_AI == "ADVANCED":
      pass
    else:
      print("Elevator AI not chosen properly!")
      print("ELEVATOR_AI: " + ELEVATOR_AI)


  def call_elevator(self, floor, direction):
    # Add to list if not already called
    if not (floor, direction) in self.queue:
      self.queue.append((floor, direction))


  def call_elevator_prediction(self, floor, target_floor):
    self.prediction_queue.append((floor, target_floor))

  def basicAI(self, waiting_list):
    free_elevators = []
    for elevator in self.elevators:
      if elevator.direction == "IDLE":
        free_elevators.append(elevator)

    for i, elevator in enumerate(free_elevators):
      elevator.go_to_floor(waiting_list[i])



  def mediumAI(self, waiting_list, walking_list):
    pass

  def advancedAI(self, waiting_list, walking_list):
    pass