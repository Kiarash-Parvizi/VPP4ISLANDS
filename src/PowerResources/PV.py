from .Resource import Resource


class PV (Resource):
    """PhotoVoltaic class from Resources
    Attributes:
    node_id     (int): node_id of bus where PV is installed
    number      (int)  : PV object number between all island PhotoVoltaic
    p_max       (float):   p_max in kW
    """
    def __init__(self, node_id: int, number: int, p_max: float) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max

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
