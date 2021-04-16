from .Resource import Resource


class WF (Resource):
    """Wind Farm class from Resources
    Attributes:
    node_id     (int)  : node_id of bus where WindFarm is installed
    number      (int)  : WF object number between all island Wind Farms
    p_max       (float): p_max in kW
    """
    def __init__(self, node_id: int, number: int, p_max: float) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max

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
