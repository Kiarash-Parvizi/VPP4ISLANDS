from .Resource import Resource
from src.Forecaster.Forecaster import Forecaster

class PV (Resource):
    """PhotoVoltaic class from Resources
    Attributes:
    node_id     (int): node_id of bus where PV is installed
    number      (int)  : PV object number between all island PhotoVoltaic
    p_max       (float): p_max in kW maximum installed power
    p_pu        (float): input type: PV Power prediction
    pr_pv       (float): output type: Kwh price Pv Installation
    """
    def __init__(self, node_id: int, number: int, p_max: float, **kwargs) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max
        # inputs
        self.p_pu = kwargs.pop('p_pu', 0)
        # outputs
        self.pr_pv = kwargs.pop('pr_pv', 0)

    def set_p_pu(self, p_pu: float) -> None:
        self.p_pu = p_pu

    def get_pr_pv(self) -> float:
        return self.pr_pv

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { "+ super().__str__() + ", p_max: " + str(self.p_max) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        """creates PV based on PV_source.csv keys and values

        Args:
            item (dict): key, value parameters

        Returns:
            PV: object of PV
        """
        number = item['PV No.']
        node_id = item['Node_id']
        p_max = item['P_max']

        return PV(node_id=node_id, number=number, p_max=p_max)

    def update_params_by_json(self, item: dict) -> None:
        """updates this object based on given item dictionary values

        Args:
            item (dict): key, value structure of the new data
        """
        self.number = item['PV No.']
        self.node_id = item['Node_id']
        self.p_max = item['P_max']

    def to_dict(self) -> dict:
        """creates a dictionary based on some of the class attributes for the
        purpose of database

        Returns:
            dict: some attributes of the PV with its values
        """
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        """creates a PV based on the given dictionary

        Args:
            _dict (dict): dictionary containing the class attributes and values

        Returns:
            Pv: PV object based on given _dict 
        """
        return PV(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        """sets the value for the given setpoint

        Args:
            key (str): key of the setpoint
            value ([type]): value of the setpoint
            w (int): w index of the setpoint
            t (int): t index of the setpoint
        """
        raise(KeyError("there is no such key for PV"))
    
    def get(self, key: str):
        """helper method for reaching the parameter values based on given key

        Args:
            key (str)

        Raises:
            KeyError: raises when the given key is not valid

        Returns:
            [type]: parameter value
        """
        # PV power generation
        if key == "P_PV":
            _data = Forecaster(self.node_id).get_pv()
            for key1, w in _data.items():
                for key2, item in w.items():
                    _data[key1][key2] = item * self.p_max / self.sbase
            return _data
        
        raise(KeyError("there is no such key for PV"))