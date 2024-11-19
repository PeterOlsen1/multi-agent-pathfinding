from board import Board
from agents import *
from optimized_agents import *
from matplotlib import pyplot as plt

def performanceLinechart(agents, iterations, board, fname, data=None):
    '''
    This function generates a line chart of the performance of each agent
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/single_runs/{fname} file.
    '''
    if data == None:
        data = board.test(iterations, agents)

    bar_labels = list(map(lambda agent: agent.__name__, agents))
    plt.figure(figsize=(12, 6))
    max_y = 0

    for agent in bar_labels:
        plt.plot(data[agent], label=agent)
        max_set = max(data[agent])
        if (max_set > max_y):
            max_y = max_set

    plt.ylim(0, max_y + (max_y * 0.1))
    plt.xlabel('Iteration')
    plt.ylabel('Time to Solution (s)')
    plt.suptitle(f'Iterations: {iterations}, Board Size: {board.rows}x{board.cols}, Number of Islands: {board.num_islands}, Island Size: [{board.min_island_size} - {board.max_island_size}]', fontsize=11)
    plt.title('Agent Performance Over Time')
    plt.legend()
    plt.savefig(f'./test_results/single_runs/{fname}')


def averagePerformanceBarChart(agents, iterations, board, fname, data=None):
    '''
    This function generates a bar chart of the AVERAGE performance of each agent
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/averages/{fname} file.

    '''
    if data == None:
        data = board.test(iterations, agents)

    averages = {}
    for agent in agents:
        total = 0
        items = 0
        for item in data[agent.__name__]:
            if item > 0:
                total += item
                items += 1
        if items > 0:
            averages[agent.__name__] = total / items
        else:
            averages[agent.__name__] = 0
    
    print(board.rows, board.cols)
    plt.figure(figsize=(12, 6))
    plt.bar(averages.keys(), averages.values())
    plt.xlabel('Agents')
    plt.suptitle(f'Iterations: {iterations}, Board Size: {board.rows}x{board.cols}, Number of Islands: {board.num_islands}, Island Size: [{board.min_island_size} - {board.max_island_size}]', fontsize=11)
    plt.ylabel('Average Performance (s)')
    plt.title(f'Average Performance of Agents')
    plt.savefig(f'./test_results/averages/{fname}')


def fastestSolutionBarChart(agents, iterations, board, fname, data=None):
    '''
    This function generates a bar chart of the number of FASTEST solutions found by each agent
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/fastest/{fname} file.
    '''
    if data == None:
        data = board.test(iterations, agents)

    fastest = {}
    for i in range(iterations):
        current_fastest = float('inf')
        current_fastest_agent = None

        for agent in agents:
            if data[agent.__name__][i] < current_fastest and data[agent.__name__][i] > 0:
                current_fastest = data[agent.__name__][i]
                current_fastest_agent = agent.__name__

        if current_fastest_agent:
            if current_fastest_agent in fastest:
                fastest[current_fastest_agent] += 1
            else:
                fastest[current_fastest_agent] = 1

    for agent in agents:
        if agent.__name__ not in fastest:
            fastest[agent.__name__] = 0


    plt.figure(figsize=(12, 6))
    plt.bar(fastest.keys(), fastest.values())
    plt.xlabel('Agents')
    plt.suptitle(f'Iterations: {iterations}, Board Size: {board.rows}x{board.cols}, Number of Islands: {board.num_islands}, Island Size: [{board.min_island_size} - {board.max_island_size}]', fontsize=11)
    plt.ylabel('# of Solutions')
    plt.title(f'# of Fastest Solutions')
    plt.savefig(f'./test_results/fastest/{fname}')


def heuristicCallsLineChart(agents, iterations, board, fname, data=None):
    '''
    This function generates a line chart of the # of times each agent called their heuristic function
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/heuristic_calls/{fname} file.
    '''
    if data == None:
        data = board.test(iterations, agents)

    bar_labels = list(map(lambda agent: agent.__name__, agents))
    plt.figure(figsize=(12, 6))
    max_y = 0

    for agent in bar_labels:
        plt.plot(data[agent + '_heuristic_calls'], label=agent)
        max_set = max(data[agent + '_heuristic_calls'])
        if (max_set > max_y):
            max_y = max_set

    plt.ylim(0, max_y + (max_y * 0.1))
    plt.xlabel('Iteration')
    plt.ylabel('# of Heuristic Calls')
    plt.suptitle(f'Iterations: {iterations}, Board Size: {board.rows}x{board.cols}, Number of Islands: {board.num_islands}, Island Size: [{board.min_island_size} - {board.max_island_size}]', fontsize=11)
    plt.title('Number of Heuristic Calls')
    plt.legend()
    plt.savefig(f'./test_results/heuristic_calls/{fname}')


def problemsSolvedBarChart(agents, iterations, board, fname, data=None):
    '''
    This function generates a bar chart of the number of problems solved by each agent
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/problems_solved/{fname} file.
    '''
    if data == None:
        data = board.test(iterations, agents)

    out = {}
    for i in range(iterations):
        for agent in agents:
            if data[agent.__name__][i] > 0:
                if agent.__name__ in out:
                    out[agent.__name__] += 1
                else:
                    out[agent.__name__] = 1

    for agent in agents:
        if agent.__name__ not in out:
            out[agent.__name__] = 0

    plt.figure(figsize=(12, 6))
    plt.bar(out.keys(), out.values())
    plt.xlabel('Agents')
    plt.suptitle(f'Iterations: {iterations}, Board Size: {board.rows}x{board.cols}, Number of Islands: {board.num_islands}, Island Size: [{board.min_island_size} - {board.max_island_size}]', fontsize=11)
    plt.ylabel('# of Problems Solved')
    plt.title(f'# of Problems Solved')
    plt.savefig(f'./test_results/problems_solved/{fname}')


if __name__ == '__main__':
    b = Board()
    b2 = Board(rows=100, cols=100, num_islands=200, min_island_size=10, max_island_size=30)
    b3 = Board(rows=1000, cols=1000, num_islands=2000, min_island_size=10, max_island_size=30)
    # agents = [AStarAgent, BidirectionalSearchAgent, GuidedLocalSearchAgent, SteepestAscentAgent]
    agents = [GuidedLocalSearchAgent, BidirectionalLocalSearchAgent]

    iterations = 1000
    board = b
    data = board.test(iterations, agents)

    averagePerformanceBarChart(agents, iterations, board, 'average_performance.png', data)
    performanceLinechart(agents, iterations, board, 'performance.png', data)
    fastestSolutionBarChart(agents, iterations, board, 'fastest.png', data)
    # problemsSolvedBarChart(agents, iterations, board, 'problems_solved.png', data)
