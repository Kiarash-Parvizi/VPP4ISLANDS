

class FixedLoad:
    """Fixed Load class
        Attributes:
        node_id         (int)  : node_id of bus where FlexibleLoads is installed
        p_consumption   (float): input type - from smart meter when installed
        pr_load         (float): output type - Kwh price
        """
    def __init__(self, node_id: int):
        self.node_id = node_id
        # input
        self.p_consumption = 0
        # output
        self.pr_load = 0

    def set_p_consumption(self, p_consumption: float) -> None:
        self.p_consumption = p_consumption

    def get_pr_load(self) -> float:
        return self.pr_load