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
    def distribute_optimizerOutput(dat):
        pass
