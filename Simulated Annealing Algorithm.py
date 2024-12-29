import random
import math
import matplotlib.pyplot as plt

def calculate_cost(state):
    cost = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                cost += 1
    return cost

def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if state[col] != row:
                new_state = list(state)
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

def simulated_annealing_with_tracking(initial_state, schedule, max_iterations=1000):
    current_state = initial_state
    current_cost = calculate_cost(current_state)
    costs = []
    temperatures = []

    for t in range(max_iterations):
        T = schedule(t)
        if T == 0:
            break

        if current_cost == 0:
            costs.append(current_cost)
            temperatures.append(T)
            print(f"Solution found at iteration {t}: {current_state} with cost {current_cost}")
            break

        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        next_cost = calculate_cost(next_state)

        ΔE = next_cost - current_cost
        acceptance_probability = math.exp(-ΔE / T) if T > 0 else 0
        accept = ΔE < 0 or random.random() < acceptance_probability

        print(f"Iteration {t}:")
        print(f"  Current state: {current_state}, Cost: {current_cost}, Temperature (T): {T}")
        print(f"  Next state: {next_state}, Next cost: {next_cost}")
        print(f"  ΔE = {ΔE}")
        print(f"  Acceptance probability: {acceptance_probability}")
        print(f"  Acceptance condition met: {accept}")

        costs.append(current_cost)
        temperatures.append(T)

        if accept:
            current_state, current_cost = next_state, next_cost

    costs.append(current_cost)
    temperatures.append(T)
    return costs, temperatures

def linear_schedule(t, initial_temp=1000, final_temp=1, max_iter=1000):
    return max(final_temp, initial_temp - (initial_temp - final_temp) * (t / max_iter))

try:
    n = int(input("Enter the number of queens (N): "))
    if n <= 0:
        raise ValueError("N must be a positive integer.")

    initial_state = list(map(int, input(f"Enter the initial state as a list of {n} integers (rows for each column): ").split()))
    if len(initial_state) != n or any(not (0 <= row < n) for row in initial_state):
        raise ValueError(f"Invalid initial state. Please provide {n} integers between 0 and {n-1}.")
except ValueError as e:
    print(e)
    n = 4
    initial_state = [random.randint(0, n - 1) for _ in range(n)]
    print(f"Using random initial state: {initial_state}")

costs, temperatures = simulated_annealing_with_tracking(initial_state, linear_schedule)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(costs, label="Objective Function (Cost)")
plt.xlabel("Iterations")
plt.ylabel("Objective Function (Cost)")
plt.title("Objective Function (Cost) over Iterations")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(temperatures, costs, label="Objective Function (Cost)")
plt.xlabel("Temperature")
plt.ylabel("Objective Function (Cost)")
plt.title("Objective Function (Cost) over Temperature")
plt.legend()

plt.tight_layout()
plt.show()

if costs[-1] == 0:
    print(f"Solution found: {initial_state}")
else:
    print("Max iterations reached without finding a solution.")

