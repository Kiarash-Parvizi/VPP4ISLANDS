from .GridNode import GridNode
from .Junction import Junction
from .VppBoxNode import VppBoxNode
from .VppNode import VppNode
from typing import AbstractSet, Tuple, List, overload, Union, Type


# interaction point between one VppNode and other components
class VppInterface:
    def __init__(self, vppNode: VppNode) -> None:
        # set other modules later
        self.vppNode = vppNode

    def get_optimizer_input_data(self):
        dat = {
            # TODO: P_PV(pv,w,t) P_Wind(wf,w,t) P/Q_L(j,t)
            'eta': {
                'ES': {
                    'Ch': 1,
                    'Dch': 2,
                }
            },
            'rho': {
                w: 'get from somewhere else'
                for w in range(1)
            },
            'lambda': {
                'DA': {
                    t: 'get from somewhere else'
                    for t in range(1)
                }
            },
        }
        gridNodes, vppBoxNodes = self.getGridNodes(), self.getVppBoxNodes()
        edgeIds = self.getEdgeIds()
        for i0, box in vppBoxNodes:
            for i1, dg in box.dg_resources.getItems():
                dat['SUC_DG'][i0][i1] = dg.get('SUC_DG')
                dat['SDC_DG'][i0][i1] = dg.get('SDC_DG')
                dat['C_DG'][i0][i1] = dg.get('C_DG')
                dat['P_DG_min'][i0][i1] = dg.get('P_DG_min')
                dat['P_DG_max'][i0][i1] = dg.get('P_DG_max')
                dat['Q_DG_min'][i0][i1] = dg.get('Q_DG_min')
                dat['Q_DG_max'][i0][i1] = dg.get('Q_DG_max')
                dat['RU_DG'][i0][i1] = dg.get('RU_DG')
                dat['RD_DG'][i0][i1] = dg.get('RD_DG')
                dat['MUT'][i0][i1] = dg.get('MUT')
                dat['MDT'][i0][i1] = dg.get('MDT')
                # P/G_L
            for i1, es in box.es_resources.getItems():
                dat['P_ChES_max'][i0][i1] = es.get('P_ChES_max')
                dat['P_DchES_max'][i0][i1] = es.get('P_DchES_max')
                dat['SOE_ES_min'][i0][i1] = es.get('SOE_ES_min')
                dat['SOE_ES_max'][i0][i1] = es.get('SOE_ES_max')
            for i1, fl in box.fl_resources.getItems():
                dat['INC'][i0][i1] = fl.get('INC')
                dat['alpha_flex'][i0][i1] = fl.get('alpha_flex')
                dat['LR_pickup'][i0][i1] = fl.get('LR_pickup')
                dat['LR_drop'][i0][i1] = fl.get('LR_drop')
            for i1, pv in box.pv_resources.getItems():
                #dat['-wt']['P_PV'][i0][i1] = dg.get('P_PV')
                pass
            for i1, wf in box.wf_resources.getItems():
                # P_Wind
                pass
            pass
        return dat
    
    # returns a list of all nodeIds of specified type in the graph
    def getNodeIds(self, type) -> List[int]:
        ls = []
        for key, val in self.vppNode.junctionMp.getItems():
            if isinstance(val, type):
                ls.append(key)
        return ls

    # returns a list of all nodeIds which are adjacent to the selected node
    def getAdjNodeIds(self, nId, type = Junction) -> List[int]:
        node = self.vppNode.junctionMp.get(nId)
        ls = []
        for eId in node.edges:
            id = self.vppNode.edgeMp.get(eId).getAdjJunction(nId)
            nd = self.vppNode.junctionMp.get(id)
            if isinstance(nd, type):
                ls.append(id)
        return ls

    # returns a list of all vppBoxNodes
    def getVppBoxNodes(self) -> List[Tuple[int, VppBoxNode]]:
        ls: List[Tuple[int, VppBoxNode]] = []
        for key, val in self.vppNode.junctionMp.getItems():
            if isinstance(val, VppBoxNode):
                ls.append((key, val))
        return ls
    # returns a list of all gridNodes
    def getGridNodes(self) -> List[Tuple[int, GridNode]]:
        ls: List[Tuple[int, GridNode]] = []
        for key, val in self.vppNode.junctionMp.getItems():
            if isinstance(val, GridNode):
                ls.append((key, val))
        return ls
    
    # returns a list of all edgesIds
    def getEdgeIds(self) -> List[int]:
        ls: List[int] = []
        for key, _ in self.vppNode.edgeMp.getItems():
            ls.append(key)
        return ls

    # change the graph and other possible related components based on setpoints
    def distribute_optimizerOutput(self, var, NW, NT, NM):
        # set func
        def setF(busObj, w: int, t: int, v):
            ''' v: gurobiVar '''
            busObj.set(v.varName, v.x, w, t)
        # tmp vars
        vppBoxNodes = self.getVppBoxNodes()
        gridNodes   = self.getGridNodes()
        # set
        for w in range(1, NW+1):
            for t in range(1, NT+1):
                L0 = var[w][t]
                # over gridNodes:
                P_DA = L0['P']['DA']
                Q_DA = L0['Q']['DA']
                for nId, obj in gridNodes:
                    setF(obj, w, t, P_DA['buy'][nId])
                    setF(obj, w, t, P_DA['sell'][nId])
                    setF(obj, w, t, Q_DA['buy'][nId])
                    setF(obj, w, t, Q_DA['sell'][nId])
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
                        for i, obj in nd.dg_resources.getItems():
                            setF(obj, w, t, P_DG[nId][i])
                            setF(obj, w, t, Q_DG[nId][i])
                            setF(obj, w, t, v_DG['SU'][nId][i])
                            setF(obj, w, t, v_DG['SD'][nId][i])
                            setF(obj, w, t, U_DG[nId][i])
                    # es
                    if nd.es_resources.len() > 0:
                        for i, obj in nd.es_resources.getItems():
                            setF(obj, w, t, P_ChES[nId][i])
                            setF(obj, w, t, P_DchES[nId][i])
                            setF(obj, w, t, SOE_ES[nId][i])
                    # fl
                    if nd.fl_resources.len() > 0:
                        for i, obj in nd.fl_resources.getItems():
                            setF(obj, w, t, P_flex[nId][i])
                            setF(obj, w, t, Q_flex[nId][i])
                    # directed edges
                    adj_nodes = self.getAdjNodeIds(nId, VppBoxNode)
                    if len(adj_nodes) != 0:
                        for nId_p in adj_nodes:
                            # TODO
                            #setF(obj, w, t, P_plus[nId][nId_p])
                            #setF(obj, w, t, P_minus[nId][nId_p])
                            #setF(obj, w, t, Q_plus[nId][nId_p])
                            #setF(obj, w, t, Q_minus[nId][nId_p])
                            # m:
                            for m in range(1, NM+1):
                                # TODO
                                #setF(obj, w, t, P_delta[nId][nId_p][m])
                                #setF(obj, w, t, Q_delta[nId][nId_p][m])
                                #setF(obj, w, t, S_delta[nId][nId_p])
                                pass
        # end of distribute_optimizerOutput
