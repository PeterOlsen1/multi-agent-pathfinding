from board import Board
from agents import *


# Testing board
# agent = DelayedImprovementAgent((255, 0, 0), 2, 3, 0, 3)
# b.agents = [agent]
# b.board = [
#     [0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 2, 2, 2, 0, 0],
#     [0, 0, 2, agent, 2, 0, 0],
#     [0, 2, 2, 0, 2, 2, 0],
#     [0, 2, 0, 0, 0, 2, 0],
#     [0, 2, 0, 0, 0, 2, 0],
#     [0, 0, 0, 0, 0, 0, 0]
# ]


# def main(agent=Agent):
#     b = Board()
#     b.generate_board()
#     b.place_agents(agent)
#     b.play(agent)

# main(BidirectionalSearchAgent)
# main()

b = Board()
print(b.test(100, AStarAgent, BidirectionalSearchAgent, SimulatedAnnealingAgent))