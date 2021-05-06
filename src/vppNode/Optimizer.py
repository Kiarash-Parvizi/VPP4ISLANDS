from .VppInterface import VppInterface

import gurobipy as gp
from gurobipy import GRB


class Optimizer:
    def __init__(self, vppInterface: VppInterface) -> None:
        self.vppInterface = vppInterface
        # create gurobi model
        self.model = gp.Model("model1")
        # add model variable
        self.__create_variables(NW=1, NT=24)
        # set objective
        self.model.setObjective(GRB.MINIMIZE)
        # set constraints
        self.set_constraints()

    def __create_variables(self, NW, NT):
        # var map
        self.var = {
            # format: w,t,['type'..],i
            w: {
                t: {
                    'P': {
                        'DA': {
                            'buy': {},
                            'sell': {},
                        },
                        'DG': {},
                        'ChES' : {}, 
                        'DchES': {},
                        'flex': {},
                        '+': {},
                        '-': {},
                    },
                    'Q': {
                        'DG': {},
                        'flex': {},
                        '+': {},
                        '-': {},
                    },
                    'v': {
                        'DG': {
                            'SU': {},
                            'SD': {},
                        },
                    },
                    'U': {
                        'DG': {},
                    },
                    'SOE': {
                        'ES': {}
                    }
                }
                for t in range(1, NT+1)
            }
            for w in range(1, NW+1)
        }

    # uses the VppInterface to retrieve input values
    def __fetch_data(self):
        self.dat = self.vppInterface.get_optimizer_input_data()

    def set_objective():
        pass

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