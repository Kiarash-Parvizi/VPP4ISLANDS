from src.PowerResources.LoadCollection import LoadColleciton
from src.vppNode.Edge import Edge
from src.Forecaster.Forecaster import Forecaster
from .Junction import Junction
from .VppBoxNode import VppBoxNode
from .VppNode import VppNode
from typing import AbstractSet, Tuple, List, overload, Union, Type

import json


# interaction point between one VppNode and other components
class VppInterface:
    def __init__(self, vppNode: VppNode) -> None:
        # set other modules later
        self.vppNode = vppNode

    # solver parameters
    def get_optimizer_input_data(self):
        forcaster = Forecaster()
        dat = {
            'P_S_L': {},
            'Q_S_L': {},
            'P_PV': {},
            'P_Wind': {},
            'eta_ES_Ch': 0.85,
            'eta_ES_Dch': 0.85,
            'rho': forcaster.get('rho'),
            'lambda_DA': forcaster.get('lambda_DA'),
            'SUC_DG': {},
            'SDC_DG': {},
            'C_DG': {},
            'P_DG_min': {},
            'P_DG_max': {},
            'Q_DG_min': {},
            'Q_DG_max': {},
            'RU_DG': {},
            'RD_DG': {},
            'MUT': {},
            'MDT': {},
            'P_ChES_max': {},
            'P_DchES_max': {},
            'SOE_ES_min': {},
            'SOE_ES_max': {},
            'INC_S': {},
            'alpha_S_flex': {},
            'LR_S_pickup': {},
            'LR_S_drop': {},
            'V_Rated': {},
            'I_max': {}, 'R': {}, 'X': {}, 'Z': {},
            'V_max': {}, 'V_min': {},
        }
        vppBoxNodes = self.getVppBoxNodes()
        edgeIds = self.getEdgeIds()
        for i0, box in vppBoxNodes:
            dat['P_PV'][i0] = {}
            dat['P_Wind'][i0] = {}
            dat['SUC_DG'][i0] = {}
            dat['SDC_DG'][i0] = {}
            dat['C_DG'][i0] = {}
            dat['P_DG_min'][i0] = {}
            dat['P_DG_max'][i0] = {}
            dat['Q_DG_min'][i0] = {}
            dat['Q_DG_max'][i0] = {}
            dat['RU_DG'][i0] = {}
            dat['RD_DG'][i0] = {}
            dat['MUT'][i0] = {}
            dat['MDT'][i0] = {}
            dat['P_ChES_max'][i0] = {} 
            dat['P_DchES_max'][i0]= {}
            dat['SOE_ES_min'][i0] = {}
            dat['SOE_ES_max'][i0] = {}
            dat['INC_S'][i0] = {}
            dat['alpha_S_flex'][i0] = {}
            dat['LR_S_pickup'][i0]  = {}
            dat['LR_S_drop'][i0] = {}
            dat['I_max'][i0]= {}; dat['R'][i0]= {}; dat['X'][i0]= {}; dat['Z'][i0]= {}
            # directed edges
            adj_nodes = self.getAdjNodeIds(i0, VppBoxNode)
            if len(adj_nodes) != 0:
                for bp in adj_nodes:
                    # form 4 left
                    # undirected edges
                    lineProps = self.getEdgeObj((i0, bp)).lineProps
                    dat['I_max'][i0][bp] = lineProps.get('I_max')
                    dat['R'][i0][bp] = lineProps.get('R')
                    dat['X'][i0][bp] = lineProps.get('X')
                    dat['Z'][i0][bp] = lineProps.get('Z')
                    pass
            # bus only
            dat['V_max'][i0] = box.get('V_max')
            dat['V_min'][i0] = box.get('V_min')
            # load container data
            # TODO change this
            if box.trade_compatible:
                print('id: ', i0, box.get('V_Rated'))
                dat['V_Rated'][i0] = box.get('V_Rated')
                continue
            load_collection = box.load_collection
            dat['INC_S'][i0] = load_collection.get('INC_S')
            dat['alpha_S_flex'][i0] = load_collection.get('alpha_S_flex')
            dat['LR_S_pickup'][i0] = load_collection.get('LR_S_pickup')
            dat['LR_S_drop'][i0] = load_collection.get('LR_S_drop')
            dat['P_S_L'][i0] = load_collection.get('P_S_L')
            dat['Q_S_L'][i0] = load_collection.get('Q_S_L')
            #
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
                # P/Q_S_L
            for i1, es in box.es_resources.getItems():
                dat['P_ChES_max'][i0][i1] = es.get('P_ChES_max')
                dat['P_DchES_max'][i0][i1] = es.get('P_DchES_max')
                dat['SOE_ES_min'][i0][i1] = es.get('SOE_ES_min')
                dat['SOE_ES_max'][i0][i1] = es.get('SOE_ES_max')
            for i1, pv in box.pv_resources.getItems():
                dat['P_PV'][i0][i1] = pv.get('P_PV')
                pass
            for i1, wf in box.wf_resources.getItems():
                dat['P_Wind'][i0][i1] = wf.get('P_Wind')
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
    
    # returns a list of all edgesIds
    def getEdgeIds(self) -> List[int]:
        ls: List[int] = []
        for key, _ in self.vppNode.edgeMp.getItems():
            ls.append(key)
        return ls

    # get edge
    def getEdgeObj(self, nodeIds: Tuple[int, int]) -> Edge:
        eId = self.vppNode.get_edgeId(nodeIds)
        return self.vppNode.edgeMp.get(eId)

    # change the graph and other possible related components based on setpoints
    def distribute_optimizerOutput(self, var, NW, NT, NM):
        # set func
        def setF(busObj, w: int, t: int, v):
            ''' v: gurobiVar '''
            busObj.set(v.varName, v.x, w, t)
        def setD(busObj, w: int, t: int, DEdge: Tuple[int,int], v):
            ''' v: gurobiVar '''
            busObj.set_dir_data(v.varName, v.x, DEdge, w, t)
        # tmp vars
        vppBoxNodes = self.getVppBoxNodes()
        # set
        for w in range(1, NW+1):
            for t in range(1, NT+1):
                L0 = var[w][t]
                # over gridNodes:
                P_DA = L0['P']['DA']
                Q_DA = L0['Q']['DA']
                # over vppBoxNodes:
                P_DG    = L0['P']['DG']
                Q_DG    = L0['Q']['DG']
                P_ChES  = L0['P']['ChES']
                P_DchES = L0['P']['DchES']
                P_S_flex= L0['P']['S']['flex']
                Q_S_flex= L0['Q']['S']['flex']
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
                    if nd.trade_compatible:
                        setF(nd, w, t, P_DA['buy'][nId])
                        setF(nd, w, t, P_DA['sell'][nId])
                        setF(nd, w, t, Q_DA['buy'][nId])
                        setF(nd, w, t, Q_DA['sell'][nId])
                        continue
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
                    loadColleciton = nd.load_collection
                    setF(loadColleciton, w, t, P_S_flex[nId])
                    setF(loadColleciton, w, t, Q_S_flex[nId])
                    # directed edges
                    adj_nodes = self.getAdjNodeIds(nId, VppBoxNode)
                    if len(adj_nodes) != 0:
                        for nId_p in adj_nodes:
                            lineProps = self.getEdgeObj((nId, nId_p)).lineProps
                            setD(lineProps, w, t, (nId,nId_p), P_plus[nId][nId_p])
                            setD(lineProps, w, t, (nId,nId_p), P_minus[nId][nId_p])
                            setD(lineProps, w, t, (nId,nId_p), Q_plus[nId][nId_p])
                            setD(lineProps, w, t, (nId,nId_p), Q_minus[nId][nId_p])
                            ## m:
                            #for m in range(1, NM+1):
                            #    # NOT NEEDED
                            #    #setF(obj, w, t, P_delta[nId][nId_p][m])
                            #    #setF(obj, w, t, Q_delta[nId][nId_p][m])
                            #    #setF(obj, w, t, S_delta[nId][nId_p])
                            pass
        # end of distribute_optimizerOutput

    def get_graph_asJson(self):
        return json.dumps(self.vppNode.to_dict())