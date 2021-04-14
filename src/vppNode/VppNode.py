from typing import Mapping, Tuple

from .LineProps import LineProps
from .Edge import Edge
from .Junction import Junction
from .Mapper import Mapper

import copy

class VppNode:
    # instance variables
    # edgeMp: Mapper[Edge]
    # junctionMp: Mapper[Junction]
    ###
    def __init__(self) -> None:
        self.edgeMp = Mapper[Edge]()
        self.junctionMp = Mapper[Junction]()

    def add_junction(self, junction: Junction) -> int:
        id = self.junctionMp.add(junction)
        return id

    def add_edge(self, junctionIds: Tuple[int,int]) -> int:
        edge = Edge(junctionIds, LineProps(100, 1, 1, 1))
        id = self.edgeMp.add(edge)
        self.junctionMp.get(junctionIds[0]).add_edge(id)
        self.junctionMp.get(junctionIds[1]).add_edge(id)
        return id

    def rem_junction(self, id: int) -> bool:
        junction = self.junctionMp.get(id)
        if self.junctionMp.rem(id):
            # remove edges connecting the removed junction to its neighbors
            eIds_toBeRemoved = []
            for eId in junction.edges:
                eIds_toBeRemoved.append(eId)
            for eId in eIds_toBeRemoved:
                self.rem_edge(eId)
            return True
        return False

    def rem_edge(self, id) -> bool:
        edge = self.edgeMp.get(id)
        if self.edgeMp.rem(id):
            for jId in edge.junctions:
                junction = self.junctionMp.get(jId)
                if junction != None:
                    junction.rem_edge(id)
            return True
        return False
    
