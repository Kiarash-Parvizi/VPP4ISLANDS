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
                            'buy': {},
                            'sell': {},
                        },
                        'DG': {},
                        'ChES' : {}, 
                        'DchES': {},
                        'flex': {},
                        '+': {},
                        '-': {},
                        'delta': {},
                    },
                    'Q': {
                        'DA': {
                            'buy': {},
                            'sell': {},
                        },
                        'DG': {},
                        'flex': {},
                        '+': {},
                        '-': {},
                        'delta': {},
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
                    },
                    'S': {
                        'delta': {},
                    },
                }
                for t in range(1, NT+1)
            }
            for w in range(1, NW+1)
        }
        #
        # asn
        for w in range(1, NW+1):
            for t in range(1, NW+1):
                L0 = self.var[w][t]
                # over gridNodes:
                P_DA = L0['P']['DA']
                Q_DA = L0['Q']['DA']
                for nId, _ in gridNodes:
                    P_DA['buy'][nId] = self.model.addVar(vtype= GRB.REAL,
                        name='%x_%x_P_DA_buy_%x'%(w,t,nId))
                    P_DA['sell'][nId] = self.model.addVar(vtype= GRB.REAL,
                        name='%x_%x_P_DA_sell_%x'%(w,t,nId))
                    Q_DA['buy'][nId] = self.model.addVar(vtype= GRB.REAL,
                        name='%x_%x_Q_DA_buy_%x'%(w,t,nId))
                    Q_DA['sell'][nId] = self.model.addVar(vtype= GRB.REAL,
                        name='%x_%x_Q_DA_sell_%x'%(w,t,nId))
                # over vppBoxNodes:
                P_DG    = L0['P']['DG']
                Q_DG    = L0['Q']['DG']
                P_ChES  = L0['P']['ChES']
                P_DchES = L0['P']['DchES']
                P_flex  = L0['P']['flex']
                Q_flex  = L0['Q']['flex']
                P_plus  = L0['P']['+']
                P_minus = L0['P']['-']
                P_delta = L0['P']['delta']
                Q_plus  = L0['P']['+']
                Q_minus = L0['P']['-']
                Q_delta = L0['Q']['delta']
                S_delta = L0['S']['delta']
                v_DG    = L0['v']['DG']
                U_DG    = L0['U']['DG']
                SOE_ES  = L0['SOE']['ES']
                for nId, nd in vppBoxNodes:
                    # dg
                    if nd.dg_resources.len() > 0:
                        P_DG[nId] = {}
                        Q_DG[nId] = {}
                        v_DG['SU'][nId] = {}
                        v_DG['SD'][nId] = {}
                        U_DG[nId] = {}
                        for i, _ in nd.dg_resources.getItems():
                            P_DG[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_P_DG_%x_%x'%(w,t,nId,i))
                            Q_DG[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_Q_DG_%x_%x'%(w,t,nId,i))
                            v_DG['SU'][nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_v_DG_SU_%x_%x'%(w,t,nId,i))
                            v_DG['SD'][nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_v_DG_SD_%x_%x'%(w,t,nId,i))
                            U_DG[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_U_DG_%x_%x'%(w,t,nId,i))
                    # es
                    if nd.es_resources.len() > 0:
                        P_ChES[nId] = {}
                        P_DchES[nId] = {}
                        SOE_ES[nId] = {}
                        for i, _ in nd.es_resources.getItems():
                            P_ChES[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_ChES_%x_%x'%(w,t,nId,i))
                            P_DchES[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_DchES_%x_%x'%(w,t,nId,i))
                            SOE_ES[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_SOE_ES_%x_%x'%(w,t,nId,i))
                    # fl
                    if nd.fl_resources.len() > 0:
                        P_flex[nId] = {}
                        Q_flex[nId] = {}
                        for i, _ in nd.fl_resources.getItems():
                            P_flex[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_P_flex_%x_%x'%(w,t,nId,i))
                            Q_flex[nId][i] = self.model.addVar(vtype= GRB.REAL,
                                name='%x_%x_Q_flex_%x_%x'%(w,t,nId,i))
                    # directed edges
                    adj_nodes = self.vppInterface.getAdjNodeIds(nId, VppBoxNode)
                    if len(adj_nodes) != 0:
                        P_plus[nId] = {}
                        Q_plus[nId] = {}
                        P_delta[nId] = {}
                        Q_delta[nId] = {}
                        S_delta[nId] = {}
                        for nId_p in adj_nodes:
                            P_delta[nId][nId_p] = {}
                            Q_delta[nId][nId_p] = {}
                            #
                            P_plus[nId][nId_p] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_+_%x_%x'%(w,t,nId,nId_p))
                            P_minus[nId][nId_p] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_-_%x_%x'%(w,t,nId,nId_p))
                            Q_plus[nId][nId_p] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_Q_+_%x_%x'%(w,t,nId,nId_p))
                            Q_minus[nId][nId_p] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_Q_-_%x_%x'%(w,t,nId,nId_p))
                            # m:
                            for m in range(1, NM+1):
                                P_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_P_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                Q_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_Q_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                S_delta[nId][nId_p] = self.model.addVar(vtype= GRB.REAL,
                                    name='%x_%x_S_delta_%x_%x'%(w,t,nId,nId_p))
        #nId: 
        #        
        #nId: self.model.addVar(vtype= GRB.REAL,
        #        ))
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
        self.rem_constraints()
        # fetch data
        self.__fetch_data()
        # add new constraints
    
    # removes old constraints
    def rem_constraints(self):
        self.model.remove(self.model.getConstrs())
    
    # uses the VppInterface to share the optimizer output with other components
    def distribute_results(self):
        self.vppInterface.distribute_optimizerOutput(self.dat)