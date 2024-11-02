from board import Board
from agents import *

b = Board()
agents = [AStarAgent, BidirectionalSearchAgent, SimulatedAnnealingAgent]
# data = b.test(100, agents)

bar_labels = list(map(lambda agent: agent.__name__, agents))
print(bar_labels)