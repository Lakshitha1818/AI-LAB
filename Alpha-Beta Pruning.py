class Node:
    def __init__(self, name, value=None, children=None):
        self.name = name
        self.value = value  # The value of the node (used for terminal nodes)
        self.children = children or []  # List of child nodes

def alpha_beta_search(state):
    def max_value(node, alpha, beta, path):
        print(f"MAX: Visiting node {node.name}, alpha={alpha}, beta={beta}")
        if terminal_test(node):
            print(f"MAX: Terminal node {node.name} has utility {utility(node)}")
            return utility(node), path
        v = float('-inf')
        best_path = []
        for child in node.children:
            value, new_path = min_value(child, alpha, beta, path + [child.name])
            print(f"MAX: From node {node.name}, child {child.name} → value={value}")
            if value > v:
                v = value
                best_path = new_path
            if v >= beta:
                print(f"MAX: Pruning at node {node.name} with value={v} ≥ beta={beta}")
                return v, best_path
            alpha = max(alpha, v)
        print(f"MAX: Returning value={v} for node {node.name}")
        return v, best_path

    def min_value(node, alpha, beta, path):
        print(f"MIN: Visiting node {node.name}, alpha={alpha}, beta={beta}")
        if terminal_test(node):
            print(f"MIN: Terminal node {node.name} has utility {utility(node)}")
            return utility(node), path
        v = float('inf')
        best_path = []
        for child in node.children:
            value, new_path = max_value(child, alpha, beta, path + [child.name])
            print(f"MIN: From node {node.name}, child {child.name} → value={value}")
            if value < v:
                v = value
                best_path = new_path
            if v <= alpha:
                print(f"MIN: Pruning at node {node.name} with value={v} ≤ alpha={alpha}")
                return v, best_path
            beta = min(beta, v)
        print(f"MIN: Returning value={v} for node {node.name}")
        return v, best_path

    print("Starting Alpha-Beta Search...\n")
    final_value, final_path = max_value(state, float('-inf'), float('inf'), [state.name])
    return final_value, final_path

# Helper Functions

# Terminal test function (checks if a node is terminal)
def terminal_test(node):
    return node.value is not None  # If the node has a value, it's a terminal node

# Utility function (returns the utility of a terminal node)
def utility(node):
    return node.value  # Return the value of the terminal node

# Example usage:

# Create the terminal nodes (leaf nodes)
H = Node('H', value=10)
I = Node('I', value=9)
J = Node('J', value=14)
K = Node('K', value=18)
L = Node('L', value=5)
M = Node('M', value=4)
N = Node('N', value=50)
O = Node('O', value=3)

# Create the non-terminal nodes with children
D = Node('D', children=[H, I])
E = Node('E', children=[J, K])
F = Node('F', children=[L, M])
G = Node('G', children=[N, O])

# Create the parent nodes
B = Node('B', children=[D, E])
C = Node('C', children=[F, G])

# Create the root node
A = Node('A', children=[B, C])

# Perform Alpha-Beta Search starting from the root node 'A'
final_value, final_path = alpha_beta_search(A)
print(f"Best path: {final_path}, with final value: {final_value}")

