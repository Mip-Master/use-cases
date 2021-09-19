"""
This is the most basic implementation of the Ukulelelala (read Ukulele-la-la) formulation.

This version uses SCIP as a solver.

Created by Aster Santana (Sep, 2021), MipMaster.org.
"""

from pyscipopt import Model, quicksum

# Input Data
# retailers
I = [1, 2, 3, 4, 5, 6, 7]
# price
p = {1: 47, 2: 65, 3: 70, 4: 68, 5: 46, 6: 78, 7: 55}
# demand
d = {1: 230, 2: 150, 3: 270, 4: 90, 5: 190, 6: 55, 7: 120}
# production upper bound
PU = 650
# shipment lower bound
SL = 50
# penalty (num. of units)
PN = 20

# Define the model
mdl = Model('Ukulele-la-la')

# Add variables
x, y = dict(), dict()
for i in I:
    x[i] = mdl.addVar(vtype='B', name=f'x_{i}')
    y[i] = mdl.addVar(vtype='I', lb= 0, name=f'y_{i}')

# Add Constraints
mdl.addCons(quicksum(y[i] for i in I) <= PU, name='max_avty')
for i in I:
    mdl.addCons(SL * x[i] <= y[i], name=f'at_least_{i}')
    mdl.addCons(y[i] <= d[i] * x[i], name=f'at_most_{i}')

# Set the objective function
revenue = sum(p[i] * y[i] for i in I)
penalty = sum((PN * p[i]) * (1 - x[i]) for i in I)
mdl.setObjective(revenue - penalty, sense='maximize')

# Optimize
mdl.optimize()

# Retrieve the solution
y_sol = {i: int(mdl.getVal(y[i])) for i in I}
print(f'y = {y_sol}')
print(f'revenue: {mdl.getVal(revenue)}')
print(f'penalty: {mdl.getVal(penalty)}')
