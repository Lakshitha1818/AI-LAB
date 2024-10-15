import heapq

# Class to represent the state of the 8-puzzle
class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board  # current board configuration
        self.parent = parent  # parent state
        self.move = move  # move made to reach this state
        self.g = g  # cost from start to this state (depth of the node)
        self.h = h  # heuristic cost to goal (Manhattan distance)
        self.f = g + h  # total cost (f = g + h)

    # Defining comparison functions for priority queue
    def __lt__(self, other):
        return self.f < other.f

# Function to print the board in a readable format
def print_board(board):
    for row in board:
        print(row)
    print()

# Function to calculate the Manhattan distance (heuristic)
def manhattan_distance(state, goal_state):
    distance = 0
    flat_goal = sum(goal_state, [])  # Flattening the 2D list into 1D
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(flat_goal.index(state[i][j]), 3)
                distance += abs(i - x) + abs(j - y)
    return distance

# Function to find the position of the blank (0) tile
def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

# Function to check if the current state is the goal state
def is_goal(state, goal_state):
    return state == goal_state

# Function to get the possible moves from the current state
def get_neighbors(state):
    neighbors = []
    row, col = find_blank(state)

    # Possible moves: Up, Down, Left, Right
    moves = [
        ('Up', (row - 1, col)),
        ('Down', (row + 1, col)),
        ('Left', (row, col - 1)),
        ('Right', (row, col + 1))
    ]

    for move, (new_row, new_col) in moves:
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in state]  # deep copy of the board
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            neighbors.append((new_state, move))

    return neighbors

# Function to print the state, g, and h values
def print_state_info(state, g, h):
    print("State:")
    print_board(state)
    print(f"g = {g}, h = {h}, f = {g + h}")
    print("-" * 20)

# A* search algorithm
def a_star(start_state, goal_state):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, PuzzleState(start_state, None, "", 0, manhattan_distance(start_state, goal_state)))

    while open_list:
        current_state = heapq.heappop(open_list)

        # Print the current state, g, and h values
        print_state_info(current_state.board, current_state.g, current_state.h)

        # Check if the current state is the goal
        if is_goal(current_state.board, goal_state):
            path = []
            while current_state.parent:
                path.append(current_state.move)
                current_state = current_state.parent
            return path[::-1]  # Return the path to the goal

        closed_set.add(tuple(map(tuple, current_state.board)))

        # Explore neighbors
        for neighbor, move in get_neighbors(current_state.board):
            if tuple(map(tuple, neighbor)) not in closed_set:
                g = current_state.g + 1  # Increment cost
                h = manhattan_distance(neighbor, goal_state)
                heapq.heappush(open_list, PuzzleState(neighbor, current_state, move, g, h))

    return None  # If no solution is found

# Example usage
if __name__ == "__main__":  # Corrected the method to check for main execution
    # Initial state of the 8-puzzle (0 represents the blank tile)
    start_state = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]

    # Goal state of the 8-puzzle
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("Start state:")
    print_board(start_state)

    print("Goal state:")
    print_board(goal_state)

    # Run A* algorithm
    solution = a_star(start_state, goal_state)

    if solution:
        print("Solution found!")
        print("Moves:", solution)
    else:
        print("No solution found.")
