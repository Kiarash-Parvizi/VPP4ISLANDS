from src.vppNode.VppBoxNode import VppBoxNode
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

    # adds a new junction to the graph
    # pure instances of junction class are not allowed 
    def add_junction(self, junction: Junction) -> int:
        id = self.junctionMp.add(junction)
        return id

    def add_junction_by_id(self, _id, junction: Junction) -> None:
        self.junctionMp.add_by_id(_id, junction)

    # adds a new undirected-edge to the graph
    def add_edge(self, junctionIds: Tuple[int,int], line: LineProps) -> int:
        edge = Edge(junctionIds, line)
        id = self.edgeMp.add(edge)
        self.junctionMp.get(junctionIds[0]).add_edge(id)
        self.junctionMp.get(junctionIds[1]).add_edge(id)
        return id

    # removes a junction with the specified id
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

    # removes an edge with the specified id
    def rem_edge(self, id) -> bool:
        edge = self.edgeMp.get(id)
        if self.edgeMp.rem(id):
            for jId in edge.junctions:
                junction = self.junctionMp.get(jId)
                if junction != None:
                    junction.rem_edge(id)
            return True
        return False
    
    # clears the graph (removes all nodes and edges)
    def clear(self) -> None:
        jLs = []
        for jId, _ in self.junctionMp.getItems():
            jLs.append(jId)
        for jId in jLs:
            self.rem_junction(jId)

    # returns the edgeId that connects two nodeIds
    def get_edgeId(self, nodeIds: Tuple[int,int]) -> int:
        nd0 = self.junctionMp.get(nodeIds[0])
        nd1 = self.junctionMp.get(nodeIds[1])
        if nd0 == None or nd1 == None:
            raise Exception('get_edgeId : err0')
        for eId in nd0.edges:
            if eId in nd1.edges:
                return eId

    # returns nodeIds which are connected by an edge with id of edgeId
    def get_nodeIds(self, edgeId) -> Tuple[int,int]:
        e0 = self.edgeMp.get(edgeId)
        if e0 == None:
            raise Exception('get_edgeId : err0')
        return e0.junctions

    # returns BusIds which are connected by an edge with id of edgeId
    def get_BusIds(self, edgeId) -> Tuple[int,int]:
        e0 = self.edgeMp.get(edgeId)
        if (e0 == None):
            raise Exception('get_BusIds : err0')
        return e0.junctions

    def to_dict(self) -> dict:
        obj = {
            'edgeMp': self.edgeMp.to_dict(),
            'junctionMp': self.junctionMp.to_dict()
        }
        return obj
    
    @staticmethod
    def create_from_dict(_dict: dict):
        # TODO: complete it
        _dict['edgeMp'] = Mapper[Edge].create_from_dict(_dict['edgeMp', Edge])
        _dict['junctionMp'] = Mapper[Junction].create_from_dict(_dict['junctionMp'], VppBoxNode)
        return 