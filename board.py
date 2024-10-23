import pygame
import random
from agent import Agent


# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))

rows, cols = 20, 20
cell_width = width // cols
cell_height = height // rows

# set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
agents = []

def make_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_board(num_islands, min_island_size, max_island_size):
    '''
    Generates the game board with the give number of islands.
    Must be used on a square board.
    '''
    intermediate = [0 for i in range(cols)]
    board = [intermediate[:] for i in range(cols)]

    for _ in range(num_islands):
        i = random.randint(1, cols - 2)
        j = random.randint(1, cols - 2)
        blocks = random.randint(min_island_size, max_island_size)
        board[i][j] = 'block'
        for _ in range(blocks - 1):
            choice_list = [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
            choice_i, choice_j = random.choice(choice_list)

            choice_in_range = 0 < choice_i < (cols - 1) and 0 < choice_j < (cols - 1)
            tries = 0

            while tries < 30 and choice_in_range and board[choice_i][choice_j] == 'block':
                choice_i, choice_j = random.choice(choice_list)
                choice_in_range = 0 < choice_i < (cols - 1) and 0 < choice_j < (cols - 1)
                tries += 1
            if choice_in_range:
                board[choice_i][choice_j] = 'block' 
    return board   

def place_agents(num_agents, board):
    for _ in range(num_agents):
        tries = 0
        i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
        while tries < 30 and board[i][j]:
            i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
            tries += 1

        tries = 0
        goal_i, goal_j = random.randint(0, rows - 1), random.randint(0, cols - 1)
        while tries < 30 and board[i][j]:
            goal_i, goal_j = random.randint(0, rows - 1), random.randint(0, cols - 1)
            tries += 1

        agent = Agent(make_random_color(), i, j, goal_i, goal_j)
        agents.append(agent)
        board[i][j] = agent


def draw_board(board):
    '''
    Draws the game board on the screen
    '''
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)

            if isinstance(board[row][col], Agent):
                agent = board[row][col]
                # draw the agent's starting position
                center = (col * cell_width + cell_width // 2, row * cell_height + cell_height // 2)
                radius = cell_height // 2 - 5
                pygame.draw.circle(screen, agent.color, center, radius)

                # draw the agent's goal position
                center = (agent.goal_i * cell_width + cell_width // 2, agent.goal_j * cell_height + cell_height // 2)
                pygame.draw.circle(screen, agent.color, center, radius)
                pygame.draw.circle(screen, WHITE, center, radius - 2)

            elif (board[row][col] ==  'block'):
                pygame.draw.rect(screen, GREY, rect)

            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    # this function call updates the entire state of the pygame window
    pygame.display.update()


board = generate_board(10, 5, 10)
place_agents(10, board)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill(WHITE)
    draw_board(board)
