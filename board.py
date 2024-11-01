import pygame
import random
from agents import Agent
import time
from copy import deepcopy

    
# set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

width = height = 800
rows = cols = 30
cell_width = width // cols
cell_height = height // rows

pygame.init()
screen = pygame.display.set_mode((width, height))

def make_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Board():
    def __init__(self, num_islands=20, min_island_size=3, max_island_size=20, display=False, num_agents=1):
        self.num_islands = num_islands
        self.min_island_size = min_island_size
        self.max_island_size = max_island_size
        self.display = display
        self.num_agents = num_agents

        self.agents = []
        self.board = []


    def generate_board(self):
        '''
        Generates the game board with the give number of islands.
        Must be used on a square board.
        '''
        intermediate = [0 for i in range(cols)]
        board = [intermediate[:] for i in range(cols)]

        def make_choice_list(i, j):
            return [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]

        for _ in range(self.num_islands):
            i = random.randint(1, cols - 2)
            j = random.randint(1, cols - 2)
            blocks = random.randint(self.min_island_size, self.max_island_size)
            board[i][j] = 2
            choice_list = make_choice_list(i, j)
            for _ in range(blocks - 1):
                choice_i, choice_j = random.choice(choice_list)

                choice_in_range = 0 < choice_i < (cols - 1) and 0 < choice_j < (cols - 1)
                tries = 0

                while tries < 10 and choice_in_range and board[choice_i][choice_j]:
                    choice_i, choice_j = random.choice(choice_list)
                    choice_in_range = 0 < choice_i < (cols - 1) and 0 < choice_j < (cols - 1)
                    tries += 1
                if choice_in_range:
                    board[choice_i][choice_j] = 2
                    choice_list = make_choice_list(choice_i, choice_j)
        self.board = deepcopy(board) 

        
    def place_agents(self, agent_class=Agent):
        '''
        Create {num_agents} agents and place them on the given board

        Parameters:
            num_agents (int): the number of agents to place on the board
            board ((Agent | int | String) [][]) the given board
        '''
        for _ in range(self.num_agents):
            tries = 0
            i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
            while tries < 30 and self.board[i][j]:
                i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
                tries += 1

            tries = 0
            goal_i, goal_j = random.randint(0, rows - 1), random.randint(0, cols - 1)
            while self.board[i][j]:
                goal_i, goal_j = random.randint(0, rows - 1), random.randint(0, cols - 1)

            agent = agent_class(make_random_color(), i, j, goal_i, goal_j)
            self.agents.append(agent)
            self.board[i][j] = agent
            self.board[goal_i][goal_j] = 1


    def draw_board(self):
        '''
        Draws the game board on the screen.

        The default square is an open white box,
        the default block is a grey block,
        and agens are rendered in two parts:
            Agent is a circle, and goal is a ring
        '''
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)

                if (self.board[row][col] == 2):
                    pygame.draw.rect(screen, GREY, rect)

                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
        for agent in self.agents:
            radius = cell_height // 2 - 5

            # draw the agent's goal position
            center = (agent.goal_j * cell_width + cell_width // 2, agent.goal_i * cell_height + cell_height // 2)
            pygame.draw.circle(screen, agent.color, center, radius)
            pygame.draw.circle(screen, WHITE, center, radius - 3)

            # draw the agent's starting position
            center = (agent.j * cell_width + cell_width // 2, agent.i * cell_height + cell_height // 2)
            pygame.draw.circle(screen, agent.color, center, radius)

        # this function call updates the entire state of the pygame window
        pygame.display.update()

    def play(self, agent_class=Agent):
        '''
        Creates a loop that initializes the board and plays until done
        '''
        # self.generate_board()
        # self.place_agents(agent_class)

        for agent in self.agents:
            agent.start_heuristic = agent.heuristic()

        # board_copy = deepcopy(board)

        screen.fill(WHITE)
        self.draw_board()
        
        # time.sleep(0.25)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == 1025:
                    self.generate_board()
                    self.agents = []
                    self.place_agents(agent_class)
            for agent in self.agents:
                agent.move(self.board)
            # time.sleep(0.1)


            screen.fill(WHITE)
            self.draw_board()
        
if __name__ == '__main__':
    b = Board()
    b.play()