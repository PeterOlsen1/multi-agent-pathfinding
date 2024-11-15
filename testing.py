from board import Board
from agents import *
from matplotlib import pyplot as plt

def performanceLinechart(agents, iterations, board, fname, data=None):
    '''
    This function generates a line chart of the performance of each agent
    for a given board and number of iterations. The results of the tests
    are saved to the /test_results/single_runs/{fname} file.
    '''
    if data == None:
        data = board.test(iterations, agents)

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
    plt.xlabel('Index')
    plt.ylabel('Value')
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
    plt.ylabel('Average Performance')
    plt.title(f'Average Performance of Agents')
    plt.savefig(f'./test_results/averages/{fname}')


if __name__ == '__main__':
    b = Board()
    b2 = Board(rows=100, cols=100, num_islands=200, min_island_size=10, max_island_size=30)
    agents = [AStarAgent, BidirectionalSearchAgent, SimulatedAnnealingAgent]
    data = b.test(100, agents)


    # averagePerformanceBarChart(agents, 10, b2, 'average_performance.png')
    performanceLinechart(agents, 100, b, 'performance.png')