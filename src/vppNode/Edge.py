from typing import Tuple
from .LineProps import LineProps

class Edge:
    # instance variables
    # junctions: Tuple[int, int]
    # lineProps: LineProps
    ###

    def __init__(self, junctions: Tuple[int, int], lineProps: LineProps) -> None:
        self.id = id
        self.junctions = junctions
        self.lineProps = lineProps

    def getAdjJunction(self, junctionId: int) -> int:
        if junctionId == self.junctions[0]:
            return self.junctions[1]
        else:
            return self.junctions[0]

    def to_dict(self):
        obj = {
            'junctions': list(self.junctions),
            'lineProps': self.lineProps.to_dict()
        }
        return obj
    
    @staticmethod  
    def create_from_dict(_dict: dict):
        _dict['junctions'] = tuple(_dict['junctions'])
        _dict['lineProps'] = LineProps.create_from_dict(_dict['lineProps'])
        return Edge(**_dict)
