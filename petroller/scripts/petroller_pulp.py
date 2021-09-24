"""
This is the most basic implementation of the Petroller formulation.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Aster Santana (Sep, 2021), MipMaster.org.
"""

import pulp

# Input Data
# crude oil sites
I = ['A', 'B']
# fuels
J = ['Regular', 'Premium', 'Jet']

# yield
r = {('A', 'Regular'): 0.20, ('A', 'Premium'): 0.23, ('A', 'Jet'): 0.25,
     ('B', 'Regular'): 0.25, ('B', 'Premium'): 0.3, ('B', 'Jet'): 0.10}
# availability
a = {'A': 2500, 'B': 3000}
# demand
d = {'Regular': 500, 'Premium': 700, 'Jet': 400}
# revenue
rv = {'Regular': 160, 'Premium': 170, 'Jet': 220}
# procurement cost
cp = {'A': 35, 'B': 42}
# unmet demand penalty
dp = {'Regular': 50, 'Premium': 65, 'Jet': 80}

# keys for x variables
x_keys = [(i, j) for i in I for j in J]

# Define the model
mdl = pulp.LpProblem('petroller', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
y = pulp.LpVariable.dicts(indexs=J, cat=pulp.LpContinuous, lowBound=0, name='y')
z = pulp.LpVariable.dicts(indexs=J, cat=pulp.LpContinuous, lowBound=0, name='z')

# oil availability
for i in I:
    mdl.addConstraint(sum(x[i, j] for j in J) <= a[i], name=f'available_{i}')
# yield of fuel
for j in J:
    mdl.addConstraint(y[j] == sum(r[i, j] * x[i, j] for i in I), name=f'yield_{j}')
# flow balance
for j in J:
    mdl.addConstraint(y[j] + z[j] >= d[j], name=f'demand_{j}')

# Set the objective function
revenue = sum(rv[j] * y[j] for j in J)
procurement = sum(cp[i] * x[i, j] for i, j in x_keys)
penalty = sum(dp[j] * z[j] for j in J)
mdl.setObjective(revenue - procurement - penalty)

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: int(x[key].value()) for key in x_keys}
y_sol = {j: int(y[j].value()) for j in J}
z_sol = {j: int(z[j].value()) for j in J}
print(f'procured = {x_sol}')
print(f'produced = {y_sol}')
print(f'outsourced = {z_sol}')
print(f'revenue: {revenue.value()}')
print(f'procurement cost: {procurement.value()}')
print(f'penalty: {penalty.value()}')
print(f'profit = {mdl.objective.value()}')
