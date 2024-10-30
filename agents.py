class Agent():
    def __init__(self, color, i, j, goal_i, goal_j):
        self.color = color
        self.i = i
        self.j = j
        self.goal_i = goal_i
        self.goal_j = goal_j
        self.frontier = []
        self.searched = set() # use a set here for faster lookup
        self.start_heuristic = 0


    def is_goal(self):
        '''
        Return True if the agent is in its goal state
        '''
        return self.i == self.goal_i and self.j == self.goal_j
    

    def heuristic(self, i=None, j=None):
        '''
        Give the straightline distance between current position and goal, ignoring obstacles
        '''
        if not i:
            i = self.i
        if not j:
            j = self.j
            
        # computing a square root is slow, make a heuristic that doesn't use it?
        return ((self.goal_i - i) ** 2 + (self.goal_j - j) ** 2) ** (1/2)
        # return max(abs(self.goal_i - i), abs(self.goal_j - j))
        

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
            check_good_heuristic = self.heuristic(i, j) < self.start_heuristic
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
        self.sort_frontier()
        
        if not self.frontier:
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.add((self.i, self.j))



    def sort_frontier(self):
        self.frontier.sort(key=lambda coord: self.heuristic(coord[0], coord[1]) + 1)


    def __repr__(self):
        return f'Agent at position ({self.i}, {self.j}) color {self.color}'
    




    
class SteepestAscentAgent(Agent):
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
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.add((self.i, self.j))






class DelayedImprovementAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j):
        '''
        In this new init function, we define 'self.iterations',
        which will increase for every local search iteration where
        we run into a local max.
        '''
        super().__init__(color, i, j, goal_i, goal_j)
        self.iterations = 0
        self.iter_cap = -float('inf')
        self.current_search = set()


    def open_moves(self, board):
        self.current_search = set() #reset this
        return self.open_moves_helper(board, self.iterations)
    
    def open_moves_helper(self, board, iteration):
        '''
        Helper function so that we can call this recursively.

        We call recursively so that we can generate 
        '''
        if not iteration:
            return []
        else:
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
            if is_valid and (check_searhced and check_good_heuristic and (not board[i][j] or board[i][j] == 1)) or not self.frontier:
                self.current_search.add((i, j))
                out.append((i, j))
                out.append(self.open_moves_helper(board, iteration - 1))
        return out
    
    
    def move(self, board):
        '''
        Moves the given agent on the board
        '''
        if self.is_goal() or self.iterations == self.iter_cap:
            return
        
        print(self.iterations)
        
        moves = self.open_moves(board)
        self.frontier += moves
        self.sort_frontier()
        
        if not self.frontier:
            self.iterations += 1
            self.frontier = self.open_moves(board)
            print(self.iterations)

            if not self.frontier:
                self.iter_cap = self.interations
                return

        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self
        self.searched.add((self.i, self.j))
    

        

class SimulatedAnnealingAgent(Agent):
    pass

if __name__ == '__main__':
    test = Agent((200, 200, 200), 0, 0, 10, 10)
    print(test.heuristic())