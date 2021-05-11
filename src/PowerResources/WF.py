from .Resource import Resource


class WF (Resource):
    """Wind Farm class from Resources
    Attributes:
    node_id     (int)  : node_id of bus where WindFarm is installed
    number      (int)  : WF object number between all island Wind Farms
    p_max       (float): p_max in kW
    p_pu        (float): input type: wind power from prediction tools
    pr_wt       (float): output type: Kwh price wind turbine
    """
    def __init__(self, node_id: int, number: int, p_max: float) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max
        # inputs
        self.p_pu = 0
        # outputs
        self.pr_wt = 0

    def set_pw_pu(self, p_pu: float) -> None:
        self.p_pu = p_pu

    def get_pr_wt(self) -> float:
        # TODO: pr_wt should send to VPPBox as an output
        return self.pr_wt

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", p_max: " + str(self.p_max) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        number = item['WF No.']
        node_id = item['Node_id']
        p_max = item['P_max']

        return WF(node_id=node_id, number=number, p_max=p_max)

    def update_params_by_json(self, item: dict) -> None:
        self.number = item['WF No.']
        self.node_id = item['Node_id']
        self.p_max = item['P_max']

    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        return WF(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        raise(KeyError("there is no such key for WF"))
    
    def get(self, key: str):
        # Wind farm Power gereration
        if key == "P_Wind":
            # TODO: ?
            return
        
        raise(KeyError("there is no such key for WF"))
