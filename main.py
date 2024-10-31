from board import Board
from agents import DelayedImprovementAgent, Agent

b = Board()
# b.generate_board()
# b.play()

# Testing board
agent = DelayedImprovementAgent((255, 0, 0), 2, 3, 0, 3)
b.agents = [agent]
b.board = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 2, 2, 2, 0, 0],
    [0, 0, 2, agent, 2, 0, 0],
    [0, 2, 2, 0, 2, 2, 0],
    [0, 2, 0, 0, 0, 2, 0],
    [0, 2, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

# b.play(DelayedImprovementAgent)
b.play()
