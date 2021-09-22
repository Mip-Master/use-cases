"""
This is the most basic implementation of the Tech Care formulation.

This version uses SCIP as a solver.

Created by Aster Santana (Sep, 2021), MipMaster.org.
"""

from pyscipopt import Model, quicksum

# Input Data
# patients
I = [1, 2, 3]
# machines
J = [1, 2]
# time periods
T = [1, 2, 3, 4]
# regular capacity
ru = {(j, t): 16 for j in J for t in T}
# overtime capacity
ou = {(j, t): 4 for j in J for t in T}
# overtime cost
oc = {(j, t): 1 for j in J for t in T}
# priority number
pn = {1: 1, 2: 2, 3: 3}
# number of sessions
ns = {1: 2, 2: 3, 3: 4}
# session duration
sd = {(1, 1): 2, (1, 2): 3, (2, 1): 2, (2, 2): 2, (2, 3): 1, (3, 1): 3, (3, 2): 2, (3, 3): 2, (3, 4): 1}
# waiting time target
wt = {1: 2, 2: 2, 3: 3}
# waiting time penalty
wp = {i: 2 * p for i, p in pn.items()}
# release time
rt = {1: 1, 2: 1, 3: 2}

# Derived data
# sessions list
sl = {i: range(1, ns[i]+1) for i in I}
# time periods list
tl = {(i, k): [t for t in T if t >= rt[i]+k-1] for i in I for k in sl[i]}
# keys for decision variables x
x_keys = [(i, j, k, t) for i, k in tl for t in tl[i, k] for j in J]
# keys for decision variables y
y_keys = [(j, t) for j in J for t in T]

# Define the model
mdl = Model('techcare')

# Add variables
x, y = dict(), dict()
for key in x_keys:
    x[key] = mdl.addVar(vtype='B', name=f'x_{key}')
for key in y_keys:
    y[key] = mdl.addVar(vtype='I', lb=0, name=f'y_{key}')

# Add Constraints
# each session must take place in at most one machine and slot
for i, k in tl:
    mdl.addCons(quicksum(x[i, j, k, t] for j in J for t in tl[i, k]) <= 1, name='sm')
# at most one session per day
for i in I:
    for t in T:
        mdl.addCons(quicksum(x[i, j, k, t] for j in J for k in sl[i] if t in tl[i, k]) <= 1, name='s')
        # mdl.addCons(quicksum(x.get((i, j, k, t), 0) for j in J for k in sl[i]) <= 1, name='s')
# Todo: implement the remaining constraints

# Set the objective function
# Todo: implement the objective function
overtime_cost = 0
total_penalty = 0
mdl.setObjective(overtime_cost - total_penalty, sense='minimize')

# Optimize
mdl.optimize()

# Retrieve the solution
x_sol = {key: int(mdl.getVal(var)) for key, var in x.items() if mdl.getVal(var) > 0.5}
print(f'x = {x_sol}')
print(f'Overtime Cost: {mdl.getVal(overtime_cost)}')
print(f'Total Penalty: {mdl.getVal(total_penalty)}')
