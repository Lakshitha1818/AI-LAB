from itertools import product

# Evaluate a logical formula using the assignment of truth values
def evaluate_formula(formula, assignment):
    return eval(formula, {}, assignment)

# Generate all possible truth assignments for the given variables
def generate_all_assignments(variables):
    return [dict(zip(variables, values)) for values in product([True, False], repeat=len(variables))]

# Create knowledge base and query from user input
def create_knowledge_base():
    print("Please enter the meanings of the following propositions:")
    p = input("Enter the meaning of proposition p : ")
    q = input("Enter the meaning of proposition q : ")
    r = input("Enter the meaning of proposition r : ")

    print(f"\nYou defined the following propositions:")
    print(f"p: {p}")
    print(f"q: {q}")
    print(f"r: {r}")

    print("\nNow, define the knowledge base (KB) and query (Q) using these propositions.")
    print("You can use 'p', 'q', 'r', 'not', 'or', 'and', and parentheses in your formulas.")

    KB = input("\nEnter the knowledge base (KB) formula : ")
    Q = input("\nEnter the query (Q) formula: ")

    return p, q, r, KB, Q

# Check if the knowledge base (KB) entails the query (Q) by evaluating the truth table
def truth_table_entailment(KB, Q, variables):
    all_assignments = generate_all_assignments(variables)

    print(f"\n{'p':<8}{'q':<8}{'r':<8}{'KB':<8}{'Q':<8}{'Entails'}")

    for assignment in all_assignments:
        KB_value = evaluate_formula(KB, assignment)
        Q_value = evaluate_formula(Q, assignment)
        entails = "Yes" if KB_value == True and Q_value == True else "No"
        print(f"{assignment['p']:<8}{assignment['q']:<8}{assignment['r']:<8}{KB_value:<8}{Q_value:<8}{entails}")

        if KB_value == True and Q_value == False:
            return False
    return True

# Main execution
if __name__ == "__main__":
    p, q, r, KB, Q = create_knowledge_base()
    variables = ['p', 'q', 'r']

    # Check if the KB entails the query Q
    result = truth_table_entailment(KB, Q, variables)

    if result:
        print("\nKB entails Q.")
    else:
        print("\nKB does not entail Q.")

