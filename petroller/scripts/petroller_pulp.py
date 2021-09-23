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
fp = {('A', 'Regular'): 0.20, ('A', 'Premium'): 0.1, ('A', 'Jet'): 0.25,
      ('B', 'Regular'): 0.25, ('B', 'Premium'): 0.3, ('B', 'Jet'): 0.10}
# availability
a = {'A': 2500, 'B': 3000}
# demand
d = {'Regular': 500, 'Premium': 700, 'Jet': 400}
# revenue
r = {'Regular': 50, 'Premium': 70, 'Jet': 120}
# procurement cost
cp = {'A': 30, 'B': 40}
# storage cost
cs = {'Regular': 2, 'Premium': 3, 'Jet': 4}
# unmet demand penalty
dp = {'Regular': 10, 'Premium': 15, 'Jet': 20}

# keys for x variables
x_keys = [(i, j) for i in I for j in J]

# Define the model
mdl = pulp.LpProblem('petroller', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
y = pulp.LpVariable.dicts(indexs=J, cat=pulp.LpContinuous, lowBound=0, name='y')
z = pulp.LpVariable.dicts(indexs=J, cat=pulp.LpContinuous, lowBound=0, name='z')
s = pulp.LpVariable.dicts(indexs=J, cat=pulp.LpContinuous, lowBound=0, name='s')

# oil availability
for i in I:
    mdl.addConstraint(sum(x[i, j] for j in J) <= a[i], name=f'oil_av_{i}')
# yield of fuel
for j in J:
    mdl.addConstraint(y[j] == sum(fp[i, j] * x[i, j] for i in I), name=f'yield_{j}')
# flow balance
for j in J:
    mdl.addConstraint(y[j] + z[j] >= s[j] + d[j], name=f'fb_{j}')

# Set the objective function
revenue = sum(r[j] * y[j] for j in J)
procurement = sum(cp[i] * x[i, j] for i, j in x_keys)
storage = sum(cs[j] * s[j] for j in J)
penalty = sum(dp[j] * z[j] for j in J)
mdl.setObjective(revenue - procurement - storage - penalty)

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: int(x[key].value()) for key in x_keys}
y_sol = {j: int(y[j].value()) for j in J}
z_sol = {j: int(z[j].value()) for j in J}
s_sol = {j: int(s[j].value()) for j in J}
print(f'procured = {x_sol}')
print(f'produced = {y_sol}')
print(f'outsourced = {z_sol}')
print(f'stored = {s_sol}')
print(f'revenue: {revenue.value()}')
print(f'procurement cost: {procurement.value()}')
print(f'storage cost: {storage.value()}')
print(f'penalty: {penalty.value()}')
print(f'profit = {mdl.objective.value()}')
