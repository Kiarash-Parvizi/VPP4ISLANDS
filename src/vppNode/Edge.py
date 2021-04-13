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
