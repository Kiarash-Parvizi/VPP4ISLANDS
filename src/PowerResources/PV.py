from .Resource import Resource


class PV (Resource):
    """PhotoVoltaic class from Resources
    Attributes:
    node_id     (int): node_id of bus where PV is installed
    number      (int)  : PV object number between all island PhotoVoltaic
    p_max       (float):   p_max in kW
    p_pu        (float): input type: PV Power prediction
    pr_wt       (float): output type: Kwh price Pv Installation
    """
    def __init__(self, node_id: int, number: int, p_max: float) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max
        # inputs
        self.p_pu = 0
        # outputs
        self.pr_pv = 0

    def set_p_pu(self, p_pu: float) -> None:
        self.p_pu = p_pu

    def get_pr_pv(self) -> float:
        return self.pr_pv

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { "+ super().__str__() + ", p_max: " + str(self.p_max) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        number = item['PV No.']
        node_id = item['Node_id']
        p_max = item['P_max']

        return PV(node_id=node_id, number=number, p_max=p_max)

    def update_params_by_json(self, item: dict) -> None:
        self.number = item['PV No.']
        self.node_id = item['Node_id']
        self.p_max = item['P_max']

    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        return PV(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        pass
    
    def get(self, key: str):
        pass