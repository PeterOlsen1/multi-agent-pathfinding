from agents import *


class MemoryLookupLocalSearchAgent(Agent):
    def __init__(self, color, i, j, goal_i, goal_j):
        super().__init__(color, i, j, goal_i, goal_j)
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


# bidirectional local search?