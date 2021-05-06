from .VppInterface import VppInterface

import gurobipy as gp
from gurobipy import GRB


class Optimizer:
    def __init__(self, vppInterface: VppInterface) -> None:
        self.vppInterface = vppInterface
        # create gurobi model
        self.model = gp.Model("model1")
        # add model variable
        self.__create_variables(NSb=1, NW=1, NT=24, NDG=10)
        # set objective
        self.model.setObjective(GRB.MINIMIZE)
        # set constraints
        self.set_constraints()

    def __create_variables(self, NW, NT, NSb, NDG):
        # var map
        self.var = {
            'P': {
                'DaBuy': {
                    # ['P']['DaBuy'][1][1][24]
                    sb: {
                        w: {
                            t: self.model.addVar(
                                vtype=GRB.REAL,
                                name='P_DaBuy_'+str(sb)+'_'+str(w)+'_'+str(t)
                               )
                            for t in range(1, NT+1)
                        }
                        for w in range(1, NW+1)
                    }
                    for sb in range(1, NSb+1)
                },
                'DaSell': {
                    # ['P']['DaSell'][1][1][24]
                    sb: {
                        w: {
                            t: self.model.addVar(
                                vtype=GRB.REAL,
                                name='P_DaSell_'+str(sb)+'_'+str(w)+'_'+str(t)
                               )
                            for t in range(1, NT+1)
                        }
                        for w in range(1, NW+1)
                    }
                    for sb in range(1, NSb+1)
                },
                'DG': {
                    # ['P']['DG'][5][1][24]
                    i: {
                        w: {
                            t: self.model.addVar(
                                vtype=GRB.REAL,
                                name='P_DG_'+str(i)+'_'+str(w)+'_'+str(t)
                               )
                            for t in range(1, NT+1)
                        }
                        for w in range(1, NW+1)
                    }
                    for i in range(1, NDG+1)
                },
            },
            'Q': {
                'DG': {
                    # ['Q']['DG'][5][1][24]
                    i: {
                        w: {
                            t: self.model.addVar(
                                vtype=GRB.REAL,
                                name='Q_DG_'+str(i)+'_'+str(w)+'_'+str(t)
                               )
                            for t in range(1, NT+1)
                        }
                        for w in range(1, NW+1)
                    }
                    for i in range(1, NDG+1)
                },
            },
            'v': {
                'DG': {
                    'SU': {
                        # ['v']['DG']['SU'][5][1][24]
                        i: {
                            w: {
                                t: self.model.addVar(
                                    vtype=GRB.REAL,
                                    name='v_DG_SU_'+str(i)+'_'+str(w)+'_'+str(t)
                                   )
                                for t in range(1, NT+1)
                            }
                            for w in range(1, NW+1)
                        }
                        for i in range(1, NDG+1)
                    },
                    'SD': {
                        # ['v']['DG']['SD'][5][1][24]
                        i: {
                            w: {
                                t: self.model.addVar(
                                    vtype=GRB.REAL,
                                    name='v_DG_SD_'+str(i)+'_'+str(w)+'_'+str(t)
                                   )
                                for t in range(1, NT+1)
                            }
                            for w in range(1, NW+1)
                        }
                        for i in range(1, NDG+1)
                    },
                },
            },
            'U': {
                'DG': {
                    # ['U']['DG'][5][1][24]
                    i: {
                        w: {
                            t: self.model.addVar(
                                vtype=GRB.REAL,
                                name='U_DG_'+str(i)+'_'+str(w)+'_'+str(t)
                               )
                            for t in range(1, NT+1)
                        }
                        for w in range(1, NW+1)
                    }
                    for i in range(1, NDG+1)
                },
            }
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