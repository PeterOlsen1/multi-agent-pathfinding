from agents import *
from functools import lru_cache

class MemoryLookupLocalSearchAgent(Agent):
    '''
    This agent is a little silly. In order to reduce the number
    of times we actually run the heuristic function, we just keep all of the
    results in a hash table. This way we only need to run the heuristic for
    a given coordinate once.

    There are definetley memory issues with this approach on larger datasets.
    '''
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.heuristics = {}
        self.penalties = {}

    def name(self):
        return 'MemoryLookupLocalSearchAgent'

    def heuristic(self, i=None, j=None):
        '''
        This heuristic function is designed so that we only need
        to actually calculate the heuristic for a given coordinate
        one time.

        Once actually calculated, store the value in a dictionary
        so that we never need to do it again.
        '''
        if i == None:
            i = self.i
        if j == None:
            j = self.j
        
        coord = (i, j)
        penalty = self.penalties.get(coord, 0)

        if (penalty > 100):
            self.no_solution = True
            return -1
    
        if coord not in self.heuristics:
            self.heuristics[coord] = super().heuristic(i, j)

        return self.heuristics[coord] * (penalty + 1)
    
    def open_moves(self, board):
        '''
        Same as open moves for local search.
        '''
        options = [
            (self.i, self.j),
            (self.i + 1, self.j),
            (self.i + 1, self.j + 1),
            (self.i + 1, self.j - 1),
            (self.i, self.j + 1),
            (self.i, self.j - 1),
            (self.i - 1, self.j + 1),
            (self.i - 1, self.j),
            (self.i - 1, self.j - 1),
        ]

        out = []
        n = len(board)
        for coord in options:
            i, j = coord
            is_valid = 0 <= i < n and 0 <= j < n
            if is_valid and (not board[i][j] or board[i][j] == 1):
                out.append(coord)
        return out
    
    def move(self, board):
        '''
        This function moves the agent. It incorporates the idea
        of penalties from GuidedLocalSearchAgent.
        '''
        if self.is_goal() or self.no_solution:
            return

        self.frontier = self.open_moves(board)
        self.sort_frontier()
        
        if not self.frontier:
            self.no_solution = True
            return
        
        coord = self.frontier.pop(0)

        if coord not in self.penalties:
            self.penalties[coord] = 1
        else:
            self.penalties[coord] += 1

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self

class CachedAStarAgent(AStarAgent):
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)

    @lru_cache(maxsize=256)
    def heuristic(self, i=None, j=None):
        '''
        Give the straightline distance between current position and goal, ignoring obstacles
        '''
        if i == None:
            i = self.i
        if j == None:
            j = self.j
        self.heuristic_calls += 1
        # computing a square root is slow, make a heuristic that doesn't use it?
        return ((self.goal_i - i) ** 2 + (self.goal_j - j) ** 2) ** (1/2)


class BidirectionalLocalSearchAgent(GuidedLocalSearchAgent):
    '''
    Perform a local search where both agents navigate to one another.

    Takes the ideas of bidirectional search and local search and combines them.
    '''
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.goal_penalties = {}

    def name(self):
        return 'BidirectionalLocalSearchAgent'
    
    def open_moves(self, board, i=None, j=None):
        '''
        Returns a list of open moves for the given board
        '''
        if i == None:
            i = self.i
        if j == None:
            j = self.j

        options = [
            (i + 1, j),
            (i + 1, j + 1),
            (i + 1, j - 1),
            (i, j + 1),
            (i, j - 1),
            (i - 1, j + 1),
            (i - 1, j),
            (i - 1, j - 1),
        ]

        out = []
        n = len(board)
        for coord in options:
            i, j = coord

            is_valid = 0 <= i and i < n and 0 <= j and j < n
            if not is_valid:
                continue

            if board[i][j] == 1 or isinstance(board[i][j], Agent):
                return [(i, j)]
            
            if (not board[i][j] or board[i][j] == 1):
                out.append(coord)
        return out
    
    def move(self, board):
        '''
        Moves the given agent on the board.

        This version will also move the goal state,
        since we are searching bidirectionally.
        '''
        if self.is_goal():
            return
        
        # get the open moves
        moves = self.open_moves(board)
        self.frontier = moves
        self.sort_frontier()

        moves = self.open_moves(board, self.goal_i, self.goal_j)
        self.goal_frontier = moves
        self.sort_goal_frontier()

        if not self.frontier or not self.goal_frontier:
            self.no_solution = True
            return
        
        coord = self.frontier.pop(0)
        goal_coord = self.goal_frontier.pop(0)

        # move agents
        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self

        # there was only one coordinate in both of them, this means we're at the goal
        # move only one agent so we don't get infinite loop
        if (not self.goal_frontier and not self.frontier):
            return

        board[self.goal_i][self.goal_j] = 0
        self.goal_i, self.goal_j = goal_coord
        board[self.goal_i][self.goal_j] = self

        # add coordinates to penalties
        if coord not in self.penalties:
            self.penalties[coord] = 1
        else:
            self.penalties[coord] += 1

        if goal_coord not in self.goal_penalties:
            self.goal_penalties[goal_coord] = 1
        else:
            self.goal_penalties[goal_coord] += 1

    def sort_goal_frontier(self):
        self.goal_frontier.sort(key=lambda coord: self.goal_heuristic(coord[0], coord[1]) + 1)

    def goal_heuristic(self, i=None, j=None):
        '''
        Redefine a new heuristic that calculates distance to the
        agent's current position.
        '''
        if i == None:
            i = self.i
        if j == None:
            j = self.j
        coord = (i, j)
        penalty = self.goal_penalties.get(coord, 0)

        if (penalty > 100):
            self.no_solution = True
            return -1

        self.heuristic_calls += 1 
              
        heuristic_val = ((self.i - i) ** 2 + (self.j - j) ** 2) ** (1/2)
        return (heuristic_val) * (penalty + 1)


class SetLookupAStarAgent(AStarAgent):
    '''
    Change data structure to a set. O(1) lookup and doesn't require as much space as a matrix
    '''
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.searched = set() # use a set here for faster lookup

    def name(self):
        return 'SetLookupAStarAgent'
    
    def move(self, board):
        '''
        Moves the given agent on the board
        '''
        if self.is_goal():
            return
        
        moves = self.open_moves(board)
        self.frontier += moves
        self.sort_frontier()
        
        if not self.frontier:
            self.no_solution = True
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.add((self.i, self.j))


class MatrixLookupAStarAgent(AStarAgent):
    '''
    Change the data structure to a matrix
    '''
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        rows = cols = len(self.board)
        self.searched = []
        for i in range(rows):
            inner = []
            for j in range(cols):
                inner.append(False)
            self.searched.append(inner)

    def name(self):
        return 'MatrixLookupAStarAgent'
    
    def move(self, board):
        '''
        Moves the given agent on the board
        '''
        if self.is_goal():
            return
        
        moves = self.open_moves(board)
        self.frontier += moves
        self.sort_frontier()
        
        if not self.frontier:
            self.no_solution = True
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.searched[self.i][self.j] = True
        self.i, self.j = coord
        board[self.i][self.j] = self

    def open_moves(self, board):
        '''
        Returns a list of open moves for the given board
        '''
        options = [
            (self.i, self.j),
            (self.i + 1, self.j),
            (self.i + 1, self.j + 1),
            (self.i + 1, self.j - 1),
            (self.i, self.j + 1),
            (self.i, self.j - 1),
            (self.i - 1, self.j + 1),
            (self.i - 1, self.j),
            (self.i - 1, self.j - 1),
        ]

        out = []
        n = len(board)
        for coord in options:
            i, j = coord
            is_valid = 0 <= i < n and 0 <= j < n
            check_searhced = is_valid and not self.searched[coord[0]][coord[1]] and coord not in self.frontier
            if is_valid and check_searhced and (not board[i][j] or board[i][j] == 1):
                out.append(coord)
        return out



def newHeuristic(self, i=None, j=None):
        '''
        Give the straightline distance between current position and goal.

        In this case, we add 1 move for every block that is found
        on the diagonal.
        '''
        if i == None:
            i = self.i
        if j == None:
            j = self.j
        self.heuristic_calls += 1
        # computing a square root is slow, make a heuristic that doesn't use it?
        step_i = (self.goal_i - i) / 10
        step_j = (self.goal_j - j) / 10

        value = ((self.goal_i - i) ** 2 + (self.goal_j - j) ** 2) ** (1/2)
        for step in range(10):
            (adjust_i, adjust_j) = (int(i + step_i * step), int(j + step_j * step))
            if (self.board[adjust_i][adjust_j] == 2):
                value += 1
        return value

class HeuristicAdjustmentAStarAgent(AStarAgent):
    def heuristic(self, i=None, j=None):
        value = newHeuristic(self, i, j)
        print(value)
        return value