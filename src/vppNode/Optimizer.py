from .GridNode import GridNode
from .VppBoxNode import VppBoxNode
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
        # tmp vars
        vppBoxNodes = self.vppInterface.getVppBoxNodes()
        gridNodes   = self.vppInterface.getGridNodes()
        edgeIds = self.vppInterface.getEdgeIds()
        # var map
        self.var = {
            # format: w,t,['type'..],i
            w: {
                t: {
                    'P': {
                        'DA': {
                            'buy': {
                                nId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_DA_buy_%x'%(w,t,nId))
                                for nId, _ in gridNodes
                            },
                            'sell': {
                                nId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_DA_sell_%x'%(w,t,nId))
                                for nId, _ in gridNodes
                            },
                        },
                        'DG': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_DG_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.dg_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.dg_resources.len() > 0
                        },
                        'ChES' : {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_ChES_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.es_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.es_resources.len() > 0
                        }, 
                        'DchES': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_DchES_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.es_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.es_resources.len() > 0
                        },
                        'flex': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_flex_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.fl_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.fl_resources.len() > 0
                        },
                        '+': {
                            eId: self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_+_%x'%(w,t,eId))
                            for eId in edgeIds
                        },
                        '-': {
                            eId: self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_-_%x'%(w,t,eId))
                            for eId in edgeIds
                        },
                    },
                    'Q': {
                        'DA': {
                            'buy': {
                                nId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_Q_DA_buy_%x'%(w,t,nId))
                                for nId, _ in gridNodes
                            },
                            'sell': {
                                nId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_Q_DA_sell_%x'%(w,t,nId))
                                for nId, _ in gridNodes
                            },
                        },
                        'DG': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_Q_DG_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.dg_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.dg_resources.len() > 0
                        },
                        'flex': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_Q_flex_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.fl_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.fl_resources.len() > 0
                        },
                        '+': {
                            eId: self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_Q_+_%x'%(w,t,eId))
                            for eId in edgeIds
                        },
                        '-': {
                            eId: self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_Q_-_%x'%(w,t,eId))
                            for eId in edgeIds
                        },
                    },
                    'v': {
                        'DG': {
                            'SU': {
                                nId: {
                                    i: self.model.addVar(vtype= GRB.REAL,
                                            name='%x_%x_v_DG_SU_%x_%x'%(w,t,nId,i))
                                    for i, _ in nd.dg_resources.getItems()
                                }
                                for nId, nd in vppBoxNodes
                                if nd.dg_resources.len() > 0
                            },
                            'SD': {
                                nId: {
                                    i: self.model.addVar(vtype= GRB.REAL,
                                            name='%x_%x_v_DG_SD_%x_%x'%(w,t,nId,i))
                                    for i, _ in nd.dg_resources.getItems()
                                }
                                for nId, nd in vppBoxNodes
                                if nd.dg_resources.len() > 0
                            },
                        },
                    },
                    'U': {
                        'DG': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_v_DG_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.dg_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.dg_resources.len() > 0
                        },
                    },
                    'SOE': {
                        'ES': {
                            nId: {
                                i: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_SOE_ES_%x_%x'%(w,t,nId,i))
                                for i, _ in nd.es_resources.getItems()
                            }
                            for nId, nd in vppBoxNodes
                            if nd.es_resources.len() > 0
                        }
                    }
                }
                for t in range(1, NT+1)
            }
            for w in range(1, NW+1)
        }
        #

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