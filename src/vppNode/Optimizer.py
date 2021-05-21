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
        # set equations
        self.set_equations()

    def __create_variables(self):
        # tmp vars
        NW, NT, NM = self.NW, self.NT, self.NM
        vppBoxNodes = self.vppInterface.getVppBoxNodes()
        # var map
        self.var = {
            # format: w,t,['type'..],i
            # var[w][t]['P']['DA']['buy'][i0][i1] = data
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
                        'S': {
                            'flex': {},
                        },
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
                        'S': {
                            'flex': {},
                        },
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
                        'ES': {},
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
            for t in range(1, NT+1):
                L0 = self.var[w][t]
                # over tradeNodes:
                P_DA = L0['P']['DA']
                Q_DA = L0['Q']['DA']
                # over vppBoxNodes:
                P_DG    = L0['P']['DG']
                Q_DG    = L0['Q']['DG']
                P_ChES  = L0['P']['ChES']
                P_DchES = L0['P']['DchES']
                P_S_flex  = L0['P']['S']['flex']
                Q_S_flex  = L0['Q']['S']['flex']
                P_plus  = L0['P']['+']
                P_minus = L0['P']['-']
                P_delta = L0['P']['delta']
                Q_plus  = L0['Q']['+']
                Q_minus = L0['Q']['-']
                Q_delta = L0['Q']['delta']
                S_delta = L0['S']['delta']
                v_DG    = L0['v']['DG']
                U_DG    = L0['U']['DG']
                SOE_ES  = L0['SOE']['ES']
                for nId, nd in vppBoxNodes:
                    # directed edges
                    adj_nodes = self.vppInterface.getAdjNodeIds(nId, VppBoxNode)
                    if len(adj_nodes) != 0:
                        P_plus[nId] = {}
                        Q_plus[nId] = {}
                        P_minus[nId] = {}
                        Q_minus[nId] = {}
                        P_delta[nId] = {}
                        Q_delta[nId] = {}
                        S_delta[nId] = {}
                        for nId_p in adj_nodes:
                            P_delta[nId][nId_p] = {}
                            Q_delta[nId][nId_p] = {}
                            #
                            P_plus[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_+_%x_%x'%(w,t,nId,nId_p))
                            P_minus[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_-_%x_%x'%(w,t,nId,nId_p))
                            Q_plus[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_Q_+_%x_%x'%(w,t,nId,nId_p))
                            Q_minus[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_Q_-_%x_%x'%(w,t,nId,nId_p))
                            # m:
                            for m in range(1, NM+1):
                                P_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                Q_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_Q_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                S_delta[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_S_delta_%x_%x'%(w,t,nId,nId_p))
                    # tradeNodes
                    if nd.trade_compatible:
                        P_DA['buy'][nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                            name='%x_%x_P_DA_buy_%x'%(w,t,nId))
                        P_DA['sell'][nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                            name='%x_%x_P_DA_sell_%x'%(w,t,nId))
                        Q_DA['buy'][nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                            name='%x_%x_Q_DA_buy_%x'%(w,t,nId))
                        Q_DA['sell'][nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                            name='%x_%x_Q_DA_sell_%x'%(w,t,nId))
                        continue
                    # dg
                    if nd.dg_resources.len() > 0:
                        P_DG[nId] = {}
                        Q_DG[nId] = {}
                        v_DG['SU'][nId] = {}
                        v_DG['SD'][nId] = {}
                        U_DG[nId] = {}
                        for i, _ in nd.dg_resources.getItems():
                            P_DG[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                name='%x_%x_P_DG_%x_%x'%(w,t,nId,i))
                            Q_DG[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                name='%x_%x_Q_DG_%x_%x'%(w,t,nId,i))
                            v_DG['SU'][nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                name='%x_%x_v_DG_SU_%x_%x'%(w,t,nId,i))
                            v_DG['SD'][nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                name='%x_%x_v_DG_SD_%x_%x'%(w,t,nId,i))
                            U_DG[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_U_DG_%x_%x'%(w,t,nId,i))
                    # es
                    if nd.es_resources.len() > 0:
                        P_ChES[nId] = {}
                        P_DchES[nId] = {}
                        SOE_ES[nId] = {}
                        for i, _ in nd.es_resources.getItems():
                            P_ChES[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_ChES_%x_%x'%(w,t,nId,i))
                            P_DchES[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_DchES_%x_%x'%(w,t,nId,i))
                            SOE_ES[nId][i] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                name='%x_%x_SOE_ES_%x_%x'%(w,t,nId,i))
                    # load
                    P_S_flex[nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                        name='%x_%x_P_S_flex_%x'%(w,t,nId))
                    Q_S_flex[nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                        name='%x_%x_Q_S_flex_%x'%(w,t,nId))
        #

    # uses the VppInterface to retrieve input values
    def __fetch_data(self):
        self.dat = self.vppInterface.get_optimizer_input_data()

    def __set_objective(self):
        # tmp vars
        NW, NT, NM = self.NW, self.NT, self.NM
        vppBoxNodes = self.vppBoxNodes
        dat, var = self.dat, self.var
        # Min Func 1:
        PMF1 = 1
        MF1 = gp.LinExpr()
        for t in range(1, NT+1):
            for i0, nd in vppBoxNodes:
                # tradeNodes
                if nd.trade_compatible:
                    L0 = var[1][t]['P']['DA']
                    MF1 += dat['lambda_DA'][t]*(L0['buy'][i0] - L0['sell'][i0])
                    continue
                # dg
                if nd.dg_resources.len() > 0:
                    for i1, _ in nd.dg_resources.getItems():
                        MF1 += dat['C_DG'][i0][i1] * var[1][t]['P']['DG'][i0][i1]
                        MF1 += dat['SUC_DG'][i0][i1] * var[1][t]['v']['DG']['SU'][i0][i1]
                        MF1 += dat['SDC_DG'][i0][i1] * var[1][t]['v']['DG']['SD'][i0][i1]
                # es
                if nd.es_resources.len() > 0:
                    #for i1, _ in nd.es_resources.getItems():
                    #    pass
                    pass
                # flex
                MF1 += var[1][t]['P']['S']['flex'][i0] * dat['INC_S'][i0]
        #
        ls: List[Tuple[float, Any]] = [
            (PMF1, MF1)
        ]
        if len(ls) != self.NW:
            raise Exception('set_objective : err0')
        ob = ls[0][1] * ls[0][0]
        for i in range(1, len(ls)):
            ob += ls[i][1] * ls[i][0]
        self.model.setObjective(ob, GRB.MINIMIZE)

    def __set_constraints(self):
        self.__rem_constraints()
        # tmp vars
        NW, NT, NM = self.NW, self.NT, self.NM
        vppBoxNodes = self.vppBoxNodes
        dat, var = self.dat, self.var
        #
        # add new constraints
        for w in range(1, NW+1):
            for t in range(1, NT+1):
                vi = var[w][t]
                for i0, nd in vppBoxNodes:
                    # vars
                    expr_sest_2_2, expr_sest_3_2 = gp.LinExpr(), gp.LinExpr()
                    # directed edges
                    adj_nodes = self.vppInterface.getAdjNodeIds(i0, VppBoxNode)
                    if len(adj_nodes) != 0:
                        for bp in adj_nodes:
                            expr_sest_2_2 += vi['P']['+'][bp][i0] - vi['P']['-'][bp][i0]
                            expr_sest_3_2 += vi['Q']['+'][bp][i0] - vi['Q']['-'][bp][i0]
                    self.model.addConstr(expr_sest_2_2==0, "c_sest_2_2_%x_%x_%x"%(w,t,i0))
                    self.model.addConstr(expr_sest_3_2==0, "c_sest_3_2_%x_%x_%x"%(w,t,i0))
                    # tradeNodes
                    if nd.trade_compatible:
                        L0 = vi['P']['DA']
                        L1 = vi['Q']['DA']
                        self.model.addConstr(L0['buy'][i0]-L0['sell'][i0]==0, "c_sest_2_%x_%x_%x"%(w,t,i0))
                        self.model.addConstr(L1['buy'][i0]-L1['sell'][i0]==0, "c_sest_3_%x_%x_%x"%(w,t,i0))
                        continue
                    # dg
                    if nd.dg_resources.len() > 0:
                        for i1, _ in nd.dg_resources.getItems():
                            expr_sest_2_2 += vi['P']['DG'][i0][i1]
                            expr_sest_3_2 += vi['Q']['DG'][i0][i1]
                            # l = NW * NT * len(dg)
                            self.model.addConstr(
                                dat['P_DG_min'][i0][i1] *
                                vi['U']['DG'][i0][i1] <=
                                vi['P']['DG'][i0][i1],
                                'c_sest_4_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            self.model.addConstr(
                                vi['P']['DG'][i0][i1] <=
                                dat['P_DG_max'][i0][i1] *
                                vi['U']['DG'][i0][i1],
                                'c_sest_4_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            self.model.addConstr(
                                dat['Q_DG_min'][i0][i1] *
                                vi['U']['DG'][i0][i1] <=
                                vi['Q']['DG'][i0][i1],
                                'c_sest_5_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            self.model.addConstr(
                                vi['Q']['DG'][i0][i1] <=
                                dat['Q_DG_max'][i0][i1] *
                                vi['U']['DG'][i0][i1],
                                'c_sest_5_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                    # es
                    if nd.pv_resources.len() > 0:
                        for i1, _ in nd.pv_resources.getItems():
                            expr_sest_2_2 += dat['P_PV'][i0][i1][w][t]
                    # es
                    if nd.es_resources.len() > 0:
                        for i1, _ in nd.es_resources.getItems():
                            expr_sest_2_2 += vi['P']['DchES'][i0][i1] - vi['P']['ChES'][i0][i1]
                            pass
                    # wf
                    if nd.wf_resources.len() > 0:
                        for i1, _ in nd.wf_resources.getItems():
                            expr_sest_2_2 += dat['P_Wind'][i0][i1][w][t]
                            pass
                    # load
        pass
    
    def set_equations(self):
        self.vppBoxNodes = self.vppInterface.getVppBoxNodes()
        # fetch data
        self.__fetch_data()
        # set equations
        self.__set_objective()
        self.__set_constraints()
    
    # removes old constraints
    def __rem_constraints(self):
        self.model.remove(self.model.getConstrs())
    
    # uses the VppInterface to share the optimizer output with other components
    def distribute_results(self):
        self.vppInterface.distribute_optimizerOutput(self.var)