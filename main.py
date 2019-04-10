from classes.simulation import Simulation
from configuration import RUN_DAYS

# Start
simulation = Simulation()
simulation.populate()
simulation.run(RUN_DAYS)