from .VppInterface import VppInterface

import gurobipy as gp
from gurobipy import GRB


class Optimizer:
    def __init__(self, vppInterface: VppInterface) -> None:
        self.vppInterface = vppInterface
        # create gurobi model
        self.model = gp.Model("model1")
        # add model variable
        # var['str'][i]
        self.model.addVar(vtype= GRB.INTEGER, name="x")
        # set objective
        #self.model.setObjective(, GRB.MINIMIZE)
        self.set_constraints()

    # uses the VppInterface to retrieve input values
    def __fetch_data(self):
        self.dat = self.vppInterface.get_optimizer_input_data()

    def set_constraints(self):
        # remove old constraints
        for constr in self.model.getContrs():
            # remove constr
            pass
        # fetch data
        self.__fetch_data()
        # add new constraints
    
    # uses the VppInterface to share the optimizer output with other components
    def distribute_results(self):
        self.vppInterface.distribute_optimizerOutput(self.dat)