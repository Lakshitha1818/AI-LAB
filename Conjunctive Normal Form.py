import re

# Helper functions to apply the transformations step by step.

# 1. Eliminate biconditionals and implications
def eliminate_biconditionals_implications(expr):
    # Eliminate biconditionals (⇔)
    expr = re.sub(r'([A-Za-z0-9()]+) ⇔ ([A-Za-z0-9()]+)', r'(\1 ⇒ \2) ∧ (\2 ⇒ \1)', expr)

    # Eliminate implications (⇒)
    expr = re.sub(r'([A-Za-z0-9()]+) ⇒ ([A-Za-z0-9()]+)', r'¬\1 ∨ \2', expr)

    return expr

# 2. Move negations inward
def move_negations_inward(expr):
    expr = re.sub(r'¬\((∀x [A-Za-z0-9()]+)\)', r'∃x ¬\1', expr)  # Move negation inside ∀
    expr = re.sub(r'¬\((∃x [A-Za-z0-9()]+)\)', r'∀x ¬\1', expr)  # Move negation inside ∃
    expr = re.sub(r'¬\(([^()]+) ∨ ([^()]+)\)', r'¬\1 ∧ ¬\2', expr)  # De Morgan's law: ¬(A ∨ B)
    expr = re.sub(r'¬\(([^()]+) ∧ ([^()]+)\)', r'¬\1 ∨ ¬\2', expr)  # De Morgan's law: ¬(A ∧ B)
    expr = re.sub(r'¬¬([A-Za-z0-9()]+)', r'\1', expr)  # Double negation elimination
    return expr

# 3. Skolemization: Replace existential quantifiers with Skolem constants/functions
def skolemize(expr):
    expr = re.sub(r'∃([A-Za-z0-9]+)', r'G1', expr)  # Replace ∃x with Skolem constant (G1)
    expr = re.sub(r'∃([A-Za-z0-9]+)\(([A-Za-z0-9, ()]+)\)', r'F1(\2)', expr)  # Existential quantifier -> Skolem function
    return expr

# 4. Drop universal quantifiers
def drop_universal_quantifiers(expr):
    expr = re.sub(r'∀([A-Za-z0-9]+)', '', expr)  # Drop ∀ quantifiers
    return expr

# 5. Distribute AND over OR to get CNF
def distribute_and_over_or(expr):
    expr = re.sub(r'(\([A-Za-z0-9()]+ ∧ [A-Za-z0-9()]+\)) ∨ ([A-Za-z0-9()]+)', r'(\1 ∨ \2)', expr)
    expr = re.sub(r'([A-Za-z0-9()]+ ∧ [A-Za-z0-9()]+) ∨ ([A-Za-z0-9()]+)', r'(\1 ∨ \2)', expr)
    return expr

# Convert to CNF using the above steps
def convert_to_cnf(expr):
    # Step 1: Eliminate biconditionals and implications
    expr = eliminate_biconditionals_implications(expr)

    # Step 2: Move negations inward
    expr = move_negations_inward(expr)

    # Step 3: Skolemize the expression
    expr = skolemize(expr)

    # Step 4: Drop universal quantifiers
    expr = drop_universal_quantifiers(expr)

    # Step 5: Distribute AND over OR to get CNF
    expr = distribute_and_over_or(expr)

    return expr

# Example FOL expressions (from the problem statement)
fol_expressions = [
    "Mary is the mother of John: Mother(Mary, John)",
    "John and Mary are both students: Student(John) ∧ Student(Mary)",
    "If it is raining, then the ground is wet: Raining ⇒ Wet(Ground)",
    "There is a person who knows every other person: ∃x ∀y (x ≠ y ⇒ Knows(x, y))",
    "Nobody is taller than themselves: ∀x ¬Taller(x, x)",
    "All students in the class passed the exam: ∀x (Student(x) ⇒ Passed(x, Exam))",
    "Mary has a pet dog: ∃x (Pet(x) ∧ Dog(x) ∧ Has(Mary, x))",
    "If Alice is a teacher, then Alice teaches mathematics: Teacher(Alice) ⇒ Teaches(Alice, Mathematics)",
    "Everyone loves someone: ∀x ∃y Loves(x, y)",
    "No one is both a teacher and a student: ∀x ¬(Teacher(x) ∧ Student(x))",
    "Every man respects his parent: ∀x (Man(x) ⇒ Respects(x, Parent(x)))",
    "Not all students like both Mathematics and Science: ¬∀x (Student(x) ⇒ (Likes(x, Mathematics) ∧ Likes(x, Science)))"
]

# Convert and print CNF for each expression
for expr in fol_expressions:
    print(f"Original FOL Expression: {expr}")
    expression = expr.split(":")[1].strip()  # Remove the description part and keep the formula
    cnf = convert_to_cnf(expression)
    print(f"CNF: {cnf}\n")
