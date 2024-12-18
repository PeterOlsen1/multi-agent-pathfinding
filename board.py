import pygame
import random
from agents import AStarAgent
import time
from copy import deepcopy

    
# set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

width = height = 600
rows = cols = 30
cell_width = width // cols
cell_height = height // rows

def make_random_color():
    '''
    Return a tuple of a random color
    '''
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Board():
    '''
    This class holds all of the necessary methods for creating a board,
    placing agents, displaying a game, and running tests.
    '''
    def __init__(self, num_islands=20, min_island_size=3, max_island_size=20, display=False, num_agents=1, rows=30, cols=30):
        self.num_islands = num_islands
        self.min_island_size = min_island_size
        self.max_island_size = max_island_size
        self.display = display
        self.num_agents = num_agents
        self.rows = rows
        self.cols = cols

        self.agents = []
        self.board = []


    def generate_board(self):
        '''
        Generates the game board with the give number of islands.
        Must be used on a square board.
        '''
        intermediate = [0 for i in range(self.cols)]
        board = [intermediate[:] for i in range(self.cols)]

        def make_choice_list(i, j):
            return [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]

        for _ in range(self.num_islands):
            i = random.randint(1, self.cols - 2)
            j = random.randint(1, self.cols - 2)
            blocks = random.randint(self.min_island_size, self.max_island_size)
            board[i][j] = 2
            choice_list = make_choice_list(i, j)
            for _ in range(blocks - 1):
                choice_i, choice_j = random.choice(choice_list)

                choice_in_range = 0 < choice_i < (self.cols - 1) and 0 < choice_j < (self.cols - 1)
                tries = 0

                while tries < 10 and choice_in_range and board[choice_i][choice_j]:
                    choice_i, choice_j = random.choice(choice_list)
                    choice_in_range = 0 < choice_i < (self.cols - 1) and 0 < choice_j < (self.cols - 1)
                    tries += 1
                if choice_in_range:
                    board[choice_i][choice_j] = 2
                    choice_list = make_choice_list(choice_i, choice_j)
        self.board = deepcopy(board) 

        
    def get_open_coords(self):
        '''
        Get open start and destination coordinates on the board.
        '''
        i, j = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        while self.board[i][j]:
            i, j = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)

        goal_i, goal_j = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        while self.board[i][j]:
            goal_i, goal_j = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)

        return [(i, j), (goal_i, goal_j)]
    
    
    def place_agents(self, agent_class=AStarAgent):
        '''
        Create {num_agents} agents and place them on the given board

        Parameters:
            num_agents (int): the number of agents to place on the board
            board ((Agent | int) [][]) the given board
        '''
        for _ in range(self.num_agents):
            [agent_coord, goal_coord] = self.get_open_coords()
            i, j = agent_coord
            goal_i, goal_j = goal_coord            

            agent = agent_class(make_random_color(), i, j, goal_i, goal_j, self.board)
            self.agents.append(agent)
            self.board[i][j] = agent
            self.board[goal_i][goal_j] = 1


    def place_single_agent(self, agent_class, i, j, goal_i, goal_j):
        '''
        Place a single agent on the board in a given position.

        Assume that the position is valid when parameters are passed in.
        '''
        agent = agent_class(make_random_color(), i, j, goal_i, goal_j, self.board)
        self.board[i][j] = agent
        self.board[goal_i][goal_j] = 1
        return agent


    def clear_agents(self):
        '''
        Remove all agents and goal states from the board.
        '''
        self.agents = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 2:
                    self.board[i][j] = 0


    def draw_board(self, screen):
        '''
        Draws the game board on the screen.

        The default square is an open white box,
        the default block is a grey block,
        and agents are rendered in two parts:
            Agent is a circle, and goal is a ring
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)

                if (self.board[row][col] == 2):
                    pygame.draw.rect(screen, GREY, rect)

                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
        for agent in self.agents:
            radius = cell_height // 2 - 5

            if (rows <= 30):
                # draw the agent's goal position
                center = (agent.goal_j * cell_width + cell_width // 2, agent.goal_i * cell_height + cell_height // 2)
                pygame.draw.circle(screen, agent.color, center, radius)
                pygame.draw.circle(screen, WHITE, center, radius - 3)

                # draw the agent's starting position
                center = (agent.j * cell_width + cell_width // 2, agent.i * cell_height + cell_height // 2)
                pygame.draw.circle(screen, agent.color, center, radius)
            else:
                goal_rect = pygame.Rect(agent.goal_j * cell_width, agent.goal_i * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, (255, 0, 0), goal_rect)

                agent_rect = pygame.Rect(agent.j * cell_width, agent.i * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, (255, 0, 0), agent_rect)

        # this function call updates the entire state of the pygame window
        pygame.display.update()


    def play(self, agent_class=AStarAgent):
        '''
        Creates a loop that initializes the board and plays until done
        '''
        pygame.init()
        screen = pygame.display.set_mode((width, height))

        for agent in self.agents:
            agent.start_heuristic = agent.heuristic()

        screen.fill(WHITE)
        self.draw_board(screen)
        
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

            time.sleep(0.1)


            screen.fill(WHITE)
            self.draw_board(screen)
        

    def test(self, iterations=10, agent_classes=[]):
        '''
        Method for testing different agent classes against each other.

        There will be no display
        '''
        out = {}
        for agent in agent_classes:
            out[agent.__name__] = []
            out[agent.__name__ + '_heuristic_calls'] = []
        
        for i in range(iterations):
            print(f'Iteration: {i}')
            self.generate_board()
            [coord, goal_coord] = self.get_open_coords()
            i, j = coord
            goal_i, goal_j = goal_coord

            for agent_class in agent_classes:
                self.clear_agents()
                agent = self.place_single_agent(agent_class, i, j, goal_i, goal_j)
                agent.start_heuristic = agent.heuristic()

                start = time.time_ns()

                # run the agent until we either find the goal or no solution
                while not agent.is_goal() and not agent.no_solution:
                    agent.move(self.board)
                end = time.time_ns()

                if agent.no_solution:
                    out[agent.name()].append(-1)
                else:
                    delta = (end - start) / 1000000
                    out[agent.name()].append(delta)
                    # print(f'finished in {delta} seconds!')

                out[agent.name() + '_heuristic_calls'].append(agent.heuristic_calls)
        return out
        