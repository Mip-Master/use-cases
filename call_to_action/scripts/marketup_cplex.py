"""
This is the most basic implementation of MarketUp formulation.

This version uses CPLEX as a solver.

Created by Rohit Karvekar (Jul 14, 21) for MipMaster.org.
"""

from docplex.mp.model import Model

# Input Data
# marketing channels
mc = {1: 'Print', 2: 'TV', 3: 'SEO', 4: 'Social Media'}
I = list(mc)
# expected ROI
r = {1: 0.16, 2: 0.09, 3: 0.06, 4: 0.14}
# expected market penetration
p = {1: 2.1, 2: 2.5, 3: 3.0, 4: 0.9}
# total budget
tb = 1_000_000
# print budget
pb = 100_000
# viewer target
vt = 1_500_000
# minimum conventional channel allocation
ca = 0.4

# Define the model
mdl = Model('market_up')

# Add variables
x = mdl.var_dict(keys=I, vartype=mdl.continuous_vartype, name='x')

# Add Constraints
# can't exceed the total budget
mdl.add_constraint(mdl.sum(x) <= tb, ctname='tb')
# minimum allocation to conventional channels
mdl.add_constraint(sum(x[i] for i in [1, 2]) >= ca * tb, ctname='ca')
# can't exceed the print budget
mdl.add_constraint(x[1] <= pb, ctname='pb')
# Social Media investment must be at most three times SEO investment
mdl.add_constraint(x[4] <= 3 * x[3], ctname='sm_seo')
# reach minimum viewers target
mdl.add_constraint(sum(p[i] * x[i] for i in I) >= vt, ctname='vt')

# Set the objective function
total_roi = sum(r[i] * x[i] for i in I)
mdl.maximize(total_roi)

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {mc[i]: int(x[i].solution_value) for i in I}
print(f'Total ROI: {total_roi.solution_value}')
print(f'Optimal budget allocation: {x_sol}')

