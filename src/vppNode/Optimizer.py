from .VppBoxNode import VppBoxNode
from .VppInterface import VppInterface
from typing import Tuple, List, Any

import gurobipy as gp
from gurobipy import GRB

import pprint

class Optimizer:
    def __init__(self, vppInterface: VppInterface) -> None:
        self.vppInterface = vppInterface
        # create gurobi model
        self.model = gp.Model("model1")
        #self.model.params.NonConvex = 2
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
                    'I2': {},
                    'V2': {},
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
                I2      = L0['I2']
                V2      = L0['V2']
                for nId, nd in vppBoxNodes:
                    # directed edges
                    adj_nodes = self.vppInterface.getAdjNodeIds(nId, VppBoxNode)
                    if len(adj_nodes) != 0:
                        P_plus[nId] = {}
                        Q_plus[nId] = {}
                        I2[nId]      = {}
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
                            I2[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_I2_%x_%x'%(w,t,nId,nId_p))
                            # m:
                            for m in range(1, NM+1):
                                P_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_P_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                Q_delta[nId][nId_p][m] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_Q_delta_%x_%x_%x'%(w,t,nId,nId_p,m))
                                S_delta[nId][nId_p] = self.model.addVar(vtype= GRB.CONTINUOUS,
                                    name='%x_%x_S_delta_%x_%x'%(w,t,nId,nId_p))
                    # bus vars
                    V2[nId] = self.model.addVar(vtype= GRB.CONTINUOUS,
                            name='%x_%x_V2_%x'%(w,t,nId))
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
        # Initialize ZeroTime vars
        for w in range(1, NW+1):
            L0 = self.var[w][0] = {}
            LP = L0['P'] = {}
            LQ = L0['Q'] = {}
            LPS = LP['S'] = {}
            LQS = LQ['S'] = {}
            LU  = L0['U'] = {}
            L_SOE  = L0['SOE'] = {}
            #
            P_S_flex = LPS['flex'] = {}
            Q_S_flex = LQS['flex'] = {}
            P_DG     = LP['DG'] = {}
            Q_DG     = LQ['DG'] = {}
            U_DG     = LU['DG'] = {}
            SOE_ES   = L_SOE['ES'] = {}
            for nId, nd in vppBoxNodes:
                # tradeNodes
                if nd.trade_compatible:
                    continue
                # load
                P_S_flex[nId] = 0.
                Q_S_flex[nId] = 0.
                # dg
                if nd.dg_resources.len() > 0:
                    P_DG[nId] = {}
                    Q_DG[nId] = {}
                    U_DG[nId] = {}
                    for i, _ in nd.dg_resources.getItems():
                        P_DG[nId][i] = 0
                        Q_DG[nId][i] = 0
                        U_DG[nId][i] = 0
                # es
                if nd.es_resources.len() > 0:
                    SOE_ES[nId] = {}
                    for i, _ in nd.es_resources.getItems():
                        SOE_ES[nId][i] = 0
        # model update
        self.model.update()

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
        #print('-'*10,'\nObj is set to : ', ob)

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
                vp = var[w][t-1]
                for i0, nd in vppBoxNodes:
                    # vars
                    expr_sest_2_2, expr_sest_3_2 = gp.LinExpr(), gp.LinExpr()
                    # directed edges
                    adj_nodes = self.vppInterface.getAdjNodeIds(i0, VppBoxNode)
                    if len(adj_nodes) != 0:
                        for bp in adj_nodes:
                            expr_sest_2_2 -= vi['P']['+'][i0][bp] - vi['P']['-'][i0][bp]
                            expr_sest_3_2 -= vi['Q']['+'][i0][bp] - vi['Q']['-'][i0][bp]
                            expr_sest_2_2 += vi['P']['+'][bp][i0] - vi['P']['-'][bp][i0]
                            expr_sest_3_2 += vi['Q']['+'][bp][i0] - vi['Q']['-'][bp][i0]
                            # form 4 left
                            self.model.addConstr(
                                vi['P']['+'][i0][bp]+vi['P']['-'][i0][bp] >= 0,
                                "c_form_4_left_%x_%x_%x_%x"%(w,t,i0,bp)
                            )
                            # form 4 right
                            self.model.addConstr(
                                vi['P']['+'][i0][bp]+vi['P']['-'][i0][bp] <=
                                dat['V_Rated'][1] * dat['I_max'][i0][bp],
                                "c_form_4_right_%x_%x_%x_%x"%(w,t,i0,bp)
                            )
                            # form 5 left
                            self.model.addConstr(
                                vi['Q']['+'][i0][bp]+vi['Q']['-'][i0][bp] >= 0,
                                "c_form_5_left_%x_%x_%x_%x"%(w,t,i0,bp)
                            )
                            # form 5 right
                            self.model.addConstr(
                                vi['Q']['+'][i0][bp]+vi['Q']['-'][i0][bp] <=
                                dat['V_Rated'][1] * dat['I_max'][i0][bp],
                                "c_form_5_right_%x_%x_%x_%x"%(w,t,i0,bp)
                            )
                            # form 6
                            #print(': ', dat['R'][i0][bp])
                            #print(': ', dat['X'][i0][bp])
                            self.model.addConstr(
                                vi['V2'][i0] - vi['V2'][bp] -
                                dat['Z'][i0][bp]**2 * vi['I2'][i0][bp] -
                                2*dat['R'][i0][bp]*(vi['P']['+'][i0][bp]-vi['P']['-'][i0][bp]) -
                                2*dat['X'][i0][bp]*(vi['Q']['+'][i0][bp]-vi['Q']['-'][i0][bp])==
                                0,
                                "c_form_6_right_%x_%x_%x_%x"%(w,t,i0,bp)
                            )
                            # undirected edges
                            expr_sest_2_2 -= dat['R'][i0][bp] * vi['I2'][i0][bp]
                            expr_sest_3_2 -= dat['X'][i0][bp] * vi['I2'][i0][bp]
                            #
                            # form 8 left
                            self.model.addConstr(
                                vi['I2'][i0][bp] >= 0,
                                'c_form_8_left_%x_%x_%x_%x'%(w,t,i0,bp)
                            )
                            # form 8 right
                            self.model.addConstr(
                                vi['I2'][i0][bp] <= dat['I_max'][i0][bp]**2,
                                'c_form_8_right_%x_%x_%x_%x'%(w,t,i0,bp)
                            )
                            # m:
                            dS = (dat['V_Rated'][1] * dat['I_max'][i0][bp]) / NM
                            expr_form_9_r, expr_form_10_r, expr_form_11_r = tuple(
                                gp.LinExpr() for _ in range(3)
                            )
                            for m in range(1, NM+1):
                                # sumations
                                expr_form_9_r += (
                                    (2*m-1) * dS * (
                                        vi['P']['delta'][i0][bp][m] +
                                        vi['Q']['delta'][i0][bp][m]
                                    )
                                )
                                expr_form_10_r += vi['P']['delta'][i0][bp][m]
                                expr_form_11_r += vi['Q']['delta'][i0][bp][m]
                                # form 12 left
                                self.model.addConstr(
                                    vi['P']['delta'][i0][bp][m] >= 0,
                                    'c_form_12_left_%x_%x_%x_%x_%x'%(w,t,i0,bp,m)
                                )
                                # form 12 right
                                self.model.addConstr(
                                    vi['P']['delta'][i0][bp][m] <= dS,
                                    'c_form_12_right_%x_%x_%x_%x_%x'%(w,t,i0,bp,m)
                                )
                                # form 13 left
                                self.model.addConstr(
                                    vi['Q']['delta'][i0][bp][m] >= 0,
                                    'c_form_13_left_%x_%x_%x_%x_%x'%(w,t,i0,bp,m)
                                )
                                # form 13 right
                                self.model.addConstr(
                                    vi['Q']['delta'][i0][bp][m] <= dS,
                                    'c_form_13_right_%x_%x_%x_%x_%x'%(w,t,i0,bp,m)
                                )
                                pass
                            # form 9
                            # TODO uncomment later
                            self.model.addConstr(
                                dat['V_Rated'][1]*vi['I2'][i0][bp] == expr_form_9_r,
                                'c_form_9_%x_%x_%x_%x'%(w,t,i0,bp)
                            )
                            # form 10
                            self.model.addConstr(
                                vi['P']['+'][i0][bp]+vi['P']['-'][i0][bp]== expr_form_10_r,
                                'c_form_10_%x_%x_%x_%x'%(w,t,i0,bp)
                            )
                            # form 11
                            self.model.addConstr(
                                vi['Q']['+'][i0][bp]+vi['Q']['-'][i0][bp]== expr_form_11_r,
                                'c_form_11_%x_%x_%x_%x'%(w,t,i0,bp)
                            )
                            pass
                    # tradeNodes
                    if nd.trade_compatible:
                        L0 = vi['P']['DA']
                        L1 = vi['Q']['DA']
                        self.model.addConstr(expr_sest_2_2 + L0['buy'][i0]-L0['sell'][i0]==0, "c_sest_2_%x_%x_%x"%(w,t,i0))
                        self.model.addConstr(expr_sest_3_2 + L1['buy'][i0]-L1['sell'][i0]==0, "c_sest_3_%x_%x_%x"%(w,t,i0))
                        continue
                    # dg
                    if nd.dg_resources.len() > 0:
                        for i1, _ in nd.dg_resources.getItems():
                            expr_sest_2_2 += vi['P']['DG'][i0][i1]
                            expr_sest_3_2 += vi['Q']['DG'][i0][i1]
                            # l = NW * NT * len(dg)
                            # sest 4 l
                            self.model.addConstr(
                                dat['P_DG_min'][i0][i1] *
                                vi['U']['DG'][i0][i1] <=
                                vi['P']['DG'][i0][i1],
                                'c_sest_4_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 4 r
                            self.model.addConstr(
                                vi['P']['DG'][i0][i1] <=
                                dat['P_DG_max'][i0][i1] *
                                vi['U']['DG'][i0][i1],
                                'c_sest_4_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 5 l
                            self.model.addConstr(
                                dat['Q_DG_min'][i0][i1] *
                                vi['U']['DG'][i0][i1] <=
                                vi['Q']['DG'][i0][i1],
                                'c_sest_5_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 5 r
                            self.model.addConstr(
                                vi['Q']['DG'][i0][i1] <=
                                dat['Q_DG_max'][i0][i1] *
                                vi['U']['DG'][i0][i1],
                                'c_sest_5_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 6
                            self.model.addConstr(
                                vi['U']['DG'][i0][i1] -
                                vp['U']['DG'][i0][i1] ==
                                vi['v']['DG']['SU'][i0][i1] -
                                vi['v']['DG']['SD'][i0][i1],
                                'c_sest_6_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 7
                            self.model.addConstr(
                                vi['v']['DG']['SU'][i0][i1] +
                                vi['v']['DG']['SD'][i0][i1] <= 1,
                                'c_sest_7_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 8
                            self.model.addConstr(
                                vi['P']['DG'][i0][i1] -
                                vp['P']['DG'][i0][i1] <=
                                dat['RU_DG'][i0][i1],
                                'c_sest_8_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 9
                            self.model.addConstr(
                                vp['P']['DG'][i0][i1] -
                                vi['P']['DG'][i0][i1] <=
                                dat['RD_DG'][i0][i1],
                                'c_sest_9_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sigma over future times
                            expr_sest_10 = gp.LinExpr(dat['MUT'][i0][i1] * (
                                vi['U']['DG'][i0][i1] -
                                vp['U']['DG'][i0][i1]))
                            expr_sest_11 = gp.LinExpr(dat['MDT'][i0][i1] * (
                                vp['U']['DG'][i0][i1] -
                                vi['U']['DG'][i0][i1]))
                            # t+1 to MUT
                            for tp in range(t+1, t+int(dat['MUT'][i0][i1])+1):
                                if tp > NT: break
                                vc = var[w][tp]
                                expr_sest_10 += (1-vc['U']['DG'][i0][i1])
                            # t+1 to MDT
                            for tp in range(t+1, t+int(dat['MDT'][i0][i1])+1):
                                if tp > NT: break
                                vc = var[w][tp]
                                expr_sest_11 += (vc['U']['DG'][i0][i1])
                            # sest 10
                            self.model.addConstr(
                                expr_sest_10 <= dat['MUT'][i0][i1],
                                'c_sest_10_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 11
                            self.model.addConstr(
                                expr_sest_11 <= dat['MDT'][i0][i1],
                                'c_sest_11_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                    # pv
                    if nd.pv_resources.len() > 0:
                        for i1, _ in nd.pv_resources.getItems():
                            expr_sest_2_2 += dat['P_PV'][i0][i1][w][t]
                    # es
                    if nd.es_resources.len() > 0:
                        for i1, _ in nd.es_resources.getItems():
                            expr_sest_2_2 += vi['P']['DchES'][i0][i1] - vi['P']['ChES'][i0][i1]
                            # sest 15 l
                            self.model.addConstr(
                                vi['P']['ChES'][i0][i1] >= 0,
                                'c_sest_15_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 15 r
                            self.model.addConstr(
                                vi['P']['ChES'][i0][i1] <=
                                dat['P_ChES_max'][i0][i1],
                                'c_sest_15_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 16 l
                            self.model.addConstr(
                                vi['P']['DchES'][i0][i1] >= 0,
                                'c_sest_16_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 16 r
                            self.model.addConstr(
                                vi['P']['DchES'][i0][i1] <=
                                dat['P_DchES_max'][i0][i1],
                                'c_sest_16_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 17
                            self.model.addConstr(
                                vi['SOE']['ES'][i0][i1] ==
                                vp['SOE']['ES'][i0][i1] +
                                (dat['eta_ES_Ch'] * vi['P']['ChES'][i0][i1]) -
                                (vi['P']['DchES'][i0][i1] / dat['eta_ES_Dch']),
                                'c_sest_17_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 18 l
                            self.model.addConstr(
                                vi['SOE']['ES'][i0][i1] >=
                                dat['SOE_ES_min'][i0][i1],
                                'c_sest_18_left_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            # sest 18 r
                            self.model.addConstr(
                                vi['SOE']['ES'][i0][i1] <=
                                dat['SOE_ES_max'][i0][i1],
                                'c_sest_18_right_%x_%x_%x_%x'%(w,t,i0,i1)
                            )
                            pass
                    # wf
                    if nd.wf_resources.len() > 0:
                        for i1, _ in nd.wf_resources.getItems():
                            expr_sest_2_2 += dat['P_Wind'][i0][i1][w][t]
                            pass
                    # load
                    expr_sest_2_2 -= dat['P_S_L'][i0][t]# - vi['P']['S']['flex'][i0]
                    expr_sest_3_2 -= dat['Q_S_L'][i0][t]# - vi['Q']['S']['flex'][i0]
                    # set constr for every bus
                    # sets 2
                    self.model.addConstr(expr_sest_2_2==0, "c_sest_2_2_%x_%x_%x"%(w,t,i0))
                    # sets 3
                    self.model.addConstr(expr_sest_3_2==0, "c_sest_3_2_%x_%x_%x"%(w,t,i0))
                    # sest 12 l
                    self.model.addConstr(
                        vi['P']['S']['flex'][i0] >= 0,
                        'c_sest_12_left_%x_%x_%x'%(w,t,i0)
                    )
                    # sest 12 r
                    self.model.addConstr(
                        vi['P']['S']['flex'][i0] <=
                        dat['alpha_S_flex'][i0] *
                        dat['P_S_L'][i0][t],
                        'c_sest_12_right_%x_%x_%x'%(w,t,i0)
                    )
                    # sest 13
                    self.model.addConstr(
                        vi['P']['S']['flex'][i0] -
                        vp['P']['S']['flex'][i0] <=
                        dat['LR_S_pickup'][i0],
                        'c_sest_13_%x_%x_%x'%(w,t,i0)
                    )
                    # sest 14
                    self.model.addConstr(
                        vp['P']['S']['flex'][i0] -
                        vi['P']['S']['flex'][i0] <=
                        dat['LR_S_drop'][i0],
                        'c_sest_14_%x_%x_%x'%(w,t,i0)
                    )
                    # form 7 left
                    self.model.addConstr(
                        vi['V2'][i0] >=
                        dat['V_min'][i0]**2,
                        'c_form_7_left_%x_%x_%x'%(w,t,i0)
                    )
                    # form 7 right
                    self.model.addConstr(
                        vi['V2'][i0] <=
                        dat['V_max'][i0]**2,
                        'c_form_7_right_%x_%x_%x'%(w,t,i0)
                    )
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

    # run the optimizer
    def optimize(self) -> None:
        self.model.optimize()
    
    # uses the VppInterface to share the optimizer output with other components
    def distribute_results(self):
        # reset ZeroTime vars
        for w in range(1, self.NW+1):
            L0 = self.var[w][0]
            L1 = self.var[w][self.NT]
            for nId, nd in self.vppBoxNodes:
                # tradeNodes
                if nd.trade_compatible:
                    continue
                # load
                L0['P']['S']['flex'][nId] = L1['P']['S']['flex'][nId].x
                L0['Q']['S']['flex'][nId] = L1['P']['S']['flex'][nId].x
                # dg
                if nd.dg_resources.len() > 0:
                    for i, _ in nd.dg_resources.getItems():
                        L0['P']['DG'][nId][i] = L1['P']['DG'][nId][i].x
                        L0['Q']['DG'][nId][i] = L1['Q']['DG'][nId][i].x
                        L0['U']['DG'][nId][i] = L1['U']['DG'][nId][i].x
                # es
                if nd.es_resources.len() > 0:
                    for i, _ in nd.es_resources.getItems():
                        #L0['SOE']['ES'][nId][i] = L1['SOE']['ES'][nId][i]
                        L0['SOE']['ES'][nId][i] = 0
        self.vppInterface.distribute_optimizerOutput(self.var, self.NW, self.NT, self.NM)