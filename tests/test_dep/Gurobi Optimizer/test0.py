import gurobipy as gp
from gurobipy import GRB

# gurobipy installation:
# gurobi912\win64> python setup.py install

# test
try:

    # Create a new model
    m = gp.Model("mip1")
    m.params.NonConvex = 2

    # Create variables
    print('OP 1:')
    x = m.addVar(vtype= GRB.INTEGER, name="x")
    y = m.addVar(vtype= GRB.INTEGER, name="y")
    z = m.addVar(vtype= GRB.INTEGER, name="z")

    # Set objective
    print('OP 2:')
    tmp = gp.LinExpr()
    tmp += x*y + 3*y + 6 * z
    tmp += 3*x*y
    m.setObjective(tmp, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    print('OP 3:')
    m.addConstr(x**2 + 2*y + 3*z <= 41, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(2*x + y**2 == 5, "c1")

    # Optimize model
    print('OP 4:')
    m.optimize()

    print('------------')
    mpd = list(map(lambda v: (v.varName, v.x), m.getVars()))
    print('mpd:', mpd)
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('------------')
    print('Obj: %g' % m.objVal)
    print('Gurobi-status: OK')

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
