import copy

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0): # Changed _init_ to __init__
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other): # Changed _lt_ to __lt__
        return self.path_cost < other.path_cost

    def expand(self):
        children = []
        row, col = self.find_blank()
        possible_actions = []
        if row > 0:
            possible_actions.append('Up')
        if row < 2:
            possible_actions.append('Down')
        if col > 0:
            possible_actions.append('Left')
        if col < 2:
            possible_actions.append('Right')

        for action in possible_actions:
            new_state = copy.deepcopy(self.state)
            if action == 'Up':
                new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
            elif action == 'Down':
                new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
            elif action == 'Left':
                new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
            elif action == 'Right':
                new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
            children.append(Node(new_state, self, action, self.path_cost + 1))
        return children

    def find_blank(self):
        for row in range(3):
            for col in range(3):
                if self.state[row][col] == 0:
                    return row, col

def depth_first_search(initial_state, goal_state):
    frontier = [Node(initial_state)]
    explored = set()

    while frontier:
        node = frontier.pop()
        if node.state == goal_state:
            return node
        explored.add(tuple(map(tuple, node.state)))
        for child in node.expand():
            if tuple(map(tuple, child.state)) not in explored:
                frontier.append(child)
    return None


def print_solution(node):
    path = []
    
    while node is not None:
        path.append((node.action, node.state))
        node = node.parent
    
    path.reverse()

    for action, state in path:
        if action:
            print(f"Action: {action}")
        for row in state:
            print(row)
        print()

initial_state = [[1, 2, 3], [4, 5, 0], [6, 7, 8]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

solution = depth_first_search(initial_state, goal_state)

if solution:
    print("Solution found:")
    print_solution(solution)
else:
    print("Solution not found.")
