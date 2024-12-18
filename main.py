from board import Board
from agents import *
from optimized_agents import *



def main(agent=Agent):
    '''
    Specify which agent to use in this main function. This will display the board
    and the agent's searching process.
    '''
    b = Board()
    # b = Board(rows=80, cols=80, num_islands=100, min_island_size=10, max_island_size=30)
    b.generate_board()
    b.place_agents(agent)
    b.play(agent)


if __name__ == '__main__':
    main(RandomLocalSearchAgent)