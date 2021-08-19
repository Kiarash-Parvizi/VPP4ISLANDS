from src.Forecaster.Forecaster import Forecaster


class FixedLoad:
    """Fixed Load class
        Attributes:
        node_id         (int)  : node_id of bus where FlexibleLoads is installed
        p_consumption   (float): input type - from smart meter when installed
        pr_load         (float): output type - Kwh price
        """

    def __init__(self, node_id: int, **kwargs):
        self.sbase = 23e5
        self.NT = 24
        self.NW = 1
        self.pf = 0.6197

        self.node_id = node_id
        # input
        self.p_consumption = kwargs.pop('p_consumption', 0)
        # output
        self.pr_load = kwargs.pop('pr_load', 0)

    def set_p_consumption(self, p_consumption: float) -> None:
        self.p_consumption = p_consumption

    def get_pr_load(self) -> float:
        return self.pr_load

    def to_dict(self) -> dict:
        return self.__dict__

    @staticmethod
    def create_from_dict(_dict: dict):
        return FixedLoad(**_dict)

    def set(self, key: str, value, w: int, t: int):
        pass

    def get(self, key: str):
        # Active loads
        if key == "P_L":
            # return Forecaster(self.node_id).get_pl()
            _data = Forecaster(self.node_id).get_pl()
            for key1, item in _data.items():
                _data[key1] = 1000 * item / self.sbase
            return _data
            
        # Reactive loads
        if key == "Q_L":
            # return Forecaster(self.node_id).get_ql()
            _data = Forecaster(self.node_id).get_ql()
            for key1, item in _data.items():
                _data[key1] = 1000 * item * self.pf / self.sbase
            return _data

        raise (KeyError("there is no such key for FixedLoad"))
