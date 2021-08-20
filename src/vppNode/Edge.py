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
        """creates a dictionary based on some of the class attributes for the
        purpose of database

        Returns:
            dict: some attributes of the Edge with its values
        """
        obj = {
            'junctions': list(self.junctions),
            'lineProps': self.lineProps.to_dict()
        }
        return obj
    
    @staticmethod  
    def create_from_dict(_dict: dict):
        """creates a Edge based on the given dictionary

        Args:
            _dict (dict): dictionary containing the class attributes and values

        Returns:
            Edge: Edge object based on given _dict 
        """
        _dict['junctions'] = tuple(_dict['junctions'])
        _dict['lineProps'] = LineProps.create_from_dict(_dict['lineProps'])
        return Edge(**_dict)
