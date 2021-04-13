from typing import Mapping, Tuple

from .LineProps import LineProps
from .Edge import Edge
from .Junction import Junction
from .Mapper import Mapper


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
        self.junctionMp.get(junctionIds[0]).edges.append(id)
        self.junctionMp.get(junctionIds[1]).edges.append(id)
        return id
