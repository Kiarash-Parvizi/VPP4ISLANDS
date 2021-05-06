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

    def get_optimizer_input_data():
        return {
            'null'
        }
    
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

    # change the graph and other possible related components based on setpoints
    def distribute_optimizerOutput(dat):
        pass
