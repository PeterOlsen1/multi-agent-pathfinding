class Agent():
    def __init__(self, color, i, j, goal_i, goal_j):
        self.color = color
        self.i = i
        self.j = j
        self.goal_i = goal_i
        self.goal_j = goal_j
        self.frontier = []


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
        return ((self.goal_i - i) ** 2 + (self.goal_j - j) ** 2) ** (1/2)
        

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
            if is_valid and not board[i][j]:
                out.append(coord)
        return out
    

    def move(self, board):
        if self.is_goal():
            return
        
        moves = self.open_moves(board)
        self.frontier += moves
        self.sort_frontier()
        if ((self.goal_i, self.goal_j) in self.frontier):
            self.i, self.j = self.goal_i, self.goal_j
            return
        coord = self.frontier.pop(0)

        board[self.i][self.j] = 0
        self.i, self.j = coord
        board[self.i][self.j] = self



    def sort_frontier(self):
        self.frontier.sort(key=lambda coord: self.heuristic(coord[0], coord[1]) + 1)

    def __repr__(self):
        return f'Agent at position ({self.i}, {self.j}) color {self.color}'
    


if __name__ == '__main__':
    test = Agent((200, 200, 200), 0, 0, 10, 10)
    print(test.heuristic())