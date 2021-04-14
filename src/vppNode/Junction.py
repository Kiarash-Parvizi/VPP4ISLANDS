from typing import Set


class Junction:
    # instance variables
    # edges : Set[int]
    ###
    
    # constructor
    def __init__(self, edges : Set[int] = None) -> None:
        self.edges = set() if edges == None else edges

    def add_edge(self, id: int):
        self.edges.add(id)
    
    def rem_edge(self, id: int) -> bool:
        if id in self.edges:
            self.edges.remove(id)
            return True
        return False

