from classes.simulation import Simulation
from configuration import RUN_DAYS

# Start
simulation = Simulation()
simulation.setup()
simulation.run(RUN_DAYS)