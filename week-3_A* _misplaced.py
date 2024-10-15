import heapq

class PuzzleState:
    def __init__(self, board, g, h, move=None, previous=None):
        self.board = board
        self.g = g  # cost to reach this node
        self.h = h  # heuristic cost (number of misplaced tiles)
        self.f = g + h  # total cost
        self.move = move  # store the move made to reach this state
        self.previous = previous  # track the previous state for path reconstruction

    def __lt__(self, other):
        return self.f < other.f  # for priority queue

    def get_blank_position(self):
        return divmod(self.board.index(0), 3)

    def generate_successors(self):
        successors = []
        x, y = self.get_blank_position()
        directions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]  # up, down, left, right
        for dx, dy, move in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = self.board[:]
                # Swap the blank space with the adjacent tile
                new_board[x * 3 + y], new_board[new_x * 3 + new_y] = new_board[new_x * 3 + new_y], new_board[x * 3 + y]
                successors.append((new_board, move))  # Append the new board and move
        return successors

    def count_misplaced_tiles(self):
        return sum(1 for i in range(9) if self.board[i] != (i + 1) % 9)  # Correctly count misplaced tiles

def a_star(initial_board, goal_board):
    initial_h = PuzzleState(initial_board, 0, 0).count_misplaced_tiles()
    initial_state = PuzzleState(initial_board, 0, initial_h)

    open_set = []
    heapq.heappush(open_set, initial_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        # Check if we reached the goal state
        if current_state.board == goal_board:
            return current_state  # Return the goal state to reconstruct the path

        closed_set.add(tuple(current_state.board))

        for successor_board, move in current_state.generate_successors():
            if tuple(successor_board) in closed_set:
                continue

            g_cost = current_state.g + 1
            h_cost = PuzzleState(successor_board, 0, 0).count_misplaced_tiles()
            successor_state = PuzzleState(successor_board, g_cost, h_cost, move, current_state)

            # Add to open set if not already present
            if not any(successor_state.board == state.board for state in open_set):
                heapq.heappush(open_set, successor_state)

    return None  # If no solution found

def print_solution(solution_state):
    path = []
    moves = []
    while solution_state:
        path.append(solution_state.board)
        moves.append(solution_state.move)
        solution_state = solution_state.previous
    
    for step, move in zip(reversed(path), reversed(moves)):
        print_board(step)
        if move:
            print("Move:", move)
    print("Solution found in", len(path) - 1, "moves.")

def print_board(board):
    for i in range(3):
        print(board[i * 3:(i + 1) * 3])
    print()

# Function to input board states from the user
def input_board(prompt):
    print(prompt)
    board = []
    for _ in range(3):  # Loop for 3 rows
        row = list(map(int, input().strip().split()))
        if len(row) != 3:
            raise ValueError("Each row must contain exactly 3 numbers.")
        board.extend(row)
    if len(board) != 9:
        raise ValueError("The board must contain exactly 9 numbers (including the blank tile).")
    return board

# Example usage:
try:
    initial_board = input_board("Enter the start state matrix (3 rows, space-separated):")
    goal_board = input_board("Enter the goal state matrix (3 rows, space-separated):")

    solution = a_star(initial_board, goal_board)

    if solution:
        print_solution(solution)
    else:
        print("No solution found.")
except Exception as e:
    print("Error:", str(e))
