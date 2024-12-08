from board import Board
from agents import *
from optimized_agents import *


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


def main(agent=Agent):
    b = Board()
    # b = Board(rows=80, cols=80, num_islands=100, min_island_size=10, max_island_size=30)
    b.generate_board()
    b.place_agents(agent)
    b.play(agent)

# main(BidirectionalSearchAgent)
# main()
# main(GuidedLocalSearchAgent)
# main(DelayedImprovementAgent)
main(HeapFrontierAStarAgent)

# b = Board()
# print(b.test(100, AStarAgent, BidirectionalSearchAgent, SimulatedAnnealingAgent))