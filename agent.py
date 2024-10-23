class Agent():
    def __init__(self, color, i, j, goal_i, goal_j):
        self.color = color
        self.i = i
        self.j = j
        self.goal_i = goal_i
        self.goal_j = goal_j

    def __repr__(self):
        return f'Agent at position ({self.i}, {self.j}) color {self.color}'