import csv
from datetime import datetime

# Format datetime to string
def tf(d):
  return d.strftime("%Y-%m-%d %H:%M:%S")

class Logger():
  def __init__(self):
    self.people_movement = []
  
  def log_people_movement(self, time, people):
    for p in people:
      if p.waiting:
        self.people_movement.append((p.id, tf(time), "WAITING", p.current_floor, p.target_floor, p.state))
      elif p.in_elevator:
        self.people_movement.append((p.id, tf(time), "IN_ELEVATOR", p.current_floor, p.target_floor, p.state))

  def get_total_waiting_time(self):
    return len(list(filter(lambda e : e[2] == "WAITING", self.people_movement)))

  def get_total_elevator_time(self):
    return len(list(filter(lambda e : e[2] == "IN_ELEVATOR", self.people_movement)))

  def save_to_file(self):
    filename = "logs/log_[{}].csv".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # filename = "generated_data.csv".format(tf(datetime.now()))

    with open(filename, mode="w") as data_file:
      data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      i = 0 # To prevent 1,000,000 logs in the case of error

      for dp in self.people_movement:
        data_writer.writerow(dp)

        if i > 5000:
          return

        i += 1
