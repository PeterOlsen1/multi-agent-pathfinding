import random
import math
import heapq

class Agent():
    '''
    Default class for an agent.

    open_moves() and move() are not defined,
    that is left to the child classes.
    '''
    def __init__(self, color, i, j, goal_i, goal_j, board):
        self.color = color
        self.i = i
        self.j = j
        self.goal_i = goal_i
        self.goal_j = goal_j
        self.frontier = []
        self.searched = []
        self.start_heuristic = 0
        self.no_solution = False
        self.heuristic_calls = 0
        self.board = board

    def name(self):
        '''
        Use this name function for hashing
        '''
        return 'Agent'

    def is_goal(self):
        '''
        Return True if the agent is in its goal state
        '''
        return self.i == self.goal_i and self.j == self.goal_j
    
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
        # return max(abs(self.goal_i - i), abs(self.goal_j - j))

    def get_choice(self, frontier, heuristic):
        '''
        Helper function to get the best choice from a frontier

        Returns a tuple of (index, value)
        '''
        best = float('inf')
        best_idx = -1
        for i in range(len(frontier)):
            coord = frontier[i]
            if heuristic(coord[0], coord[1]) < best:
                best = heuristic(coord[0], coord[1])
                best_idx = i

        return best_idx
    
    def open_moves(self, board):
        pass
    
    def move(self, board):
        pass

    def sort_frontier(self):
        self.frontier.sort(key=lambda coord: self.heuristic(coord[0], coord[1]) + 1)
    
    def __repr__(self):
        return f'Agent at position ({self.i}, {self.j}) color {self.color}'
    

class AStarAgent(Agent):
    def name(self):
        '''
        Use this name function for hashing
        '''
        return 'AStarAgent'
        
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
            check_searhced = coord not in self.searched and coord not in self.frontier
            if is_valid and check_searhced and (not board[i][j] or board[i][j] == 1):
                out.append(coord)
        return out
    

    def move(self, board):
        '''
        Moves the given agent on the board
        '''
        if self.is_goal():
            return
        
        moves = self.open_moves(board)
        self.frontier += moves
        
        if not self.frontier:
            self.no_solution = True
            return
        
        idx = self.get_choice(self.frontier, self.heuristic)
        coord = self.frontier.pop(idx)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.append((self.i, self.j))


class BidirectionalSearchAgent(Agent):
    '''
    This search agent is a little different. 

    We will employ A* but from both ways. This way 
    we can search towards each other instead of one direction
    at a time.
    '''    
    def __init__(self, color, i, j, goal_i, goal_j, board):
        '''
        In this new init function, we define 'self.iterations',
        which will increase for every local search iteration where
        we run into a local max.

        The value 'self.iterations' reflects the radius of the surrouding
        spaces we will search for a move after running into a local max
        '''
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.goal_frontier = []
        self.goal_searched = []
    
    def name(self):
        return 'BidirectionalSearchAgent'
        
    def open_moves(self, board, i=None, j=None, goal=False):
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

            check_searhced = coord not in self.searched and coord not in self.frontier

            if goal:
                check_searhced = coord not in self.goal_searched and coord not in self.goal_frontier

            if board[i][j] == 1 or isinstance(board[i][j], Agent):
                self.frontier = [(i, j)]
                self.goal_frontier = [(i, j)]
                return []
                # return [coord]
            
            if check_searhced and (not board[i][j] or board[i][j] == 1):
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
        
        moves = self.open_moves(board)
        self.frontier += moves

        moves = self.open_moves(board, self.goal_i, self.goal_j, True)
        self.goal_frontier += moves
        
        if not self.frontier or not self.goal_frontier:
            self.no_solution = True
            return
        
        idx = self.get_choice(self.frontier, self.heuristic)
        coord = self.frontier.pop(idx)

        idx = self.get_choice(self.goal_frontier, self.goal_heuristic)
        goal_coord = self.goal_frontier.pop(idx)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self

        board[self.goal_i][self.goal_j] = 0
        self.goal_i, self.goal_j = goal_coord
        board[self.goal_i][self.goal_j] = self

        self.searched.append((self.i, self.j))
        self.goal_searched.append((self.goal_i, self.goal_j))


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

        self.heuristic_calls += 1        
        return ((self.i - i) ** 2 + (self.j - j) ** 2) ** (1/2)


''' =================================== LOCAL SEARCH AGENTS =================================== 
    Agents defined below are local search agents. They do not keep track of old searches, and only
    search for the best move from the current state.
'''
    
class SteepestAscentAgent(Agent):
    def name(self):
        return 'SteepestAscentAgent'
    
    def open_moves(self, board):
        '''
        Returns a list of open moves for the given board.

        Because of steepest ascent hill climb rules, we only
        check out moves that are closer to the goal than we are.
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
            check_searhced = coord not in self.searched and coord not in self.frontier
            check_good_heuristic = self.heuristic(i, j) < self.heuristic()
            if is_valid and check_searhced and check_good_heuristic and (not board[i][j] or board[i][j] == 1):
                out.append(coord)
        return out
    
    def move(self, board):
        '''
        Moves the given agent on the board.

        This version is adapted to only search spaces near to the agent
        This uses steepest ascent hill climb local search.
        '''

        if self.is_goal():
            return

        self.frontier = self.open_moves(board)
        
        if not self.frontier:
            self.no_solution = True
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self



class DelayedImprovementAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j, board):
        '''
        In this new init function, we define 'self.iterations',
        which will increase for every local search iteration where
        we run into a local max.

        The value 'self.iterations' reflects the radius of the surrouding
        spaces we will search for a move after running into a local max
        '''
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.iterations = 2
        self.iter_cap = 100

    def name(self):
        return 'DelayedImprovementAgent'

    def open_moves(self, board):
        '''
        Call the helper function to generate possible moves from our current state.

        Still local search since the current_search set is only used to find
        nodes in the current search, and not keep track of old searches.
        '''
        self.current_search = set()
        moves = self.open_moves_helper(board, self.iterations)
        out = []
        for move in moves:
            if self.heuristic(move[0], move[1]) < self.heuristic():
                out.append(move)
        return out
    
    def open_moves_helper(self, board, iteration, i=None, j=None):
        '''
        Helper function so that we can call this recursively.

        We call recursively so that we can generate all moves
        in some given radius from the current point.

        Default parameters are used with I and J so that
        if we don't pass in any values, they will default to the
        current position. However, if we do pass in values, we
        will calculate new moves from the given position.
        '''
        if iteration <= 0:
            return []
        else:

            if i == None:
                i = self.i
            if j == None:
                j = self.j

            options = [
            (i, j),
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
            if not coord:
                pass
            i, j = coord
            is_valid = 0 <= i < n and 0 <= j < n
            check_searhced = coord not in self.current_search
            if is_valid and (check_searhced and (not board[i][j] or board[i][j] == 1)):
                self.current_search.add((i, j))
                out.append((i, j))
                res = self.open_moves_helper(board, iteration - 1, i, j) # don't immediatley return bc we need to check if its empty or not
                if res:
                    out += res
        return out
    
    
    def move(self, board):
        '''
        Moves the given agent on the board

        This function is updated so that the frontier
        is only ever the current moves we can do from our position,
        or our moves within the radius defined by 'self.iterations'.

        '''
        if self.is_goal() or self.iterations == self.iter_cap:
            # if we're at the cap, there is no solution
            self.no_solution = (self.iterations == self.iter_cap)
            return
                
        self.frontier = self.open_moves(board)

        if not self.frontier:
            self.iterations += 1
            self.frontier = self.open_moves(board)

            # frontier is still empty. return so that we can move again
            if not self.frontier:
                return

        idx = self.get_choice(self.frontier, self.heuristic)
        coord = self.frontier.pop(idx)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.add((self.i, self.j))
    


class SimulatedAnnealingAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j, board):
        '''
        In this new init function, we define 'self.iterations',
        which will increase for every local search iteration where
        we run into a local max.

        The value 'self.iterations' reflects the radius of the surrounding
        spaces we will search for a move after running into a local max
        '''
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.iterations = 1
        self.temp = 1000
        self.repeats = 0

    def name(self):
        return 'SimulatedAnnealingAgent'

    def open_moves(self, board):
        '''
        Returns a list of open moves for the given board.

        Duplicate the method here so that we don't check 'self.searched',
        so that this can still be local search
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
                heapq.heappush(out, (self.heuristic(i, j), coord))
        return out
    

    def move(self, board):
        '''
        Moves the given agent on the board
        '''
        if self.is_goal():
            return
        
        self.frontier = self.open_moves(board)
        self.sort_frontier()
        
        if not self.frontier or self.repeats > 10:
            self.no_solution = True
            return
        
        # we've hit a high level of iterations but no solution, we are likely stuck
        # reset to bring back randomness
        if self.iterations > 1000:
            self.repeats += 1
            self.iterations = 1

        T = self.temp / self.iterations
        n = len(self.frontier)

        idx_to_pop = 0
        coord = self.frontier[0]

        # give a weighted choice so that the simulated annealing can lend itself towards more optimal move
        if n > 1:
            weighted_choice = []
            for i in range(n - 1, 0, -1):
                for j in range(i):
                    weighted_choice.append(n - i)

            # next_idx = random.choice(weighted_choice)
            # next = self.frontier[next_idx]

            next = random.choice(self.frontier)
            next_idx = self.frontier.index(next)

            delta = self.heuristic(coord[0], coord[1]) - self.heuristic(next[0], next[1])

            if delta > 0:
                idx_to_pop = next_idx
                coord = next
            elif random.random() < math.exp(delta / T):
                idx_to_pop = next_idx
                coord = next
        self.iterations += 1
        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.frontier.pop(idx_to_pop)


class GuidedLocalSearchAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.penalties = {}

    def name(self):
        return 'GuidedLocalSearchAgent'
    
    def heuristic(self, i=None, j=None):
        if i == None:
            i = self.i
        if j == None:
            j = self.j

        # grab heuristic so we only need to calculate it once
        heuristic_val = super().heuristic(i, j)
        straight_line = heuristic_val
        penalty = self.penalties.get((i, j), 0)

        # we've visited the same square 100 times. time to stop
        if (penalty > 100):
            self.no_solution = True
            return -1
        return straight_line + penalty * heuristic_val
    
    def open_moves(self, board):
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
        Moves the given agent on the board.
        '''
        if self.is_goal() or self.no_solution:
            return

        self.frontier = self.open_moves(board)
        
        if not self.frontier:
            self.no_solution = True
            return
        
        idx = self.get_choice(self.frontier, self.heuristic)
        coord = self.frontier.pop(idx)

        if coord not in self.penalties:
            self.penalties[coord] = 1
        else:
            self.penalties[coord] += 1

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self


class RandomLocalSearchAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j, board):
        super().__init__(color, i, j, goal_i, goal_j, board)
        self.moves = 0

    def name(self):
        return 'RandomLocalSearchAgent'
    
    def open_moves(self, board):
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
        Moves the given agent on the board.
        '''
        if self.is_goal() or self.no_solution or self.moves > 1000000:
            return

        self.moves += 1
        self.frontier = self.open_moves(board)
        
        if not self.frontier:
            self.no_solution = True
            return
        
        coord = random.choice(self.frontier)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self

if __name__ == '__main__':
    test = Agent((200, 200, 200), 0, 0, 10, 10)
    print(test.heuristic())