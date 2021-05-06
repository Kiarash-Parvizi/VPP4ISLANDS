from .GridNode import GridNode
from .VppBoxNode import VppBoxNode
from .VppInterface import VppInterface
from typing import Tuple, List, Any

import gurobipy as gp
from gurobipy import GRB


class Optimizer:
    def __init__(self, vppInterface: VppInterface) -> None:
        self.vppInterface = vppInterface
        # create gurobi model
        self.model = gp.Model("model1")
        # add model variable
        self.NW, self.NT, self.NM = 1, 24, 20
        self.__create_variables()
        # set objective
        self.set_objective()
        # set constraints
        self.set_constraints()

    def __create_variables(self):
        # tmp vars
        NW, NT, NM = self.NW, self.NT, self.NM
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
                        'delta': {
                            m: {
                                eId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_P_delta_%x_%x'%(w,t,m,eId))
                                for eId in edgeIds
                            }
                            for m in range(1, NM+1)
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
                        'delta': {
                            m: {
                                eId: self.model.addVar(vtype= GRB.REAL,
                                        name='%x_%x_Q_delta_%x_%x'%(w,t,m,eId))
                                for eId in edgeIds
                            }
                            for m in range(1, NM+1)
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
                    },
                    'S': {
                        'delta': {
                            eId: self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_S_delta_%x'%(w,t,eId))
                            for eId in edgeIds
                        },
                    },
                }
                for t in range(1, NT+1)
            }
            for w in range(1, NW+1)
        }
        #

    # uses the VppInterface to retrieve input values
    def __fetch_data(self):
        self.dat = self.vppInterface.get_optimizer_input_data()

    def set_objective(self):
        ls: List[Tuple[float, Any]] = [
        ]
        if len(ls) != self.NW:
            raise Exception('set_objective : err0')
        ob = ls[0][1] * ls[0][0]
        for i in range(1, len(ls)):
            ob += ls[i][1] * ls[i][0]
        self.model.setObjective(ob, GRB.MINIMIZE)

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