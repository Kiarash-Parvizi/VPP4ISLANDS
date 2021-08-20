from .Resource import Resource
from src.vppNode.Mapper import Mapper


class FL(Resource):
    """Flexible Load class from Resources
    Attributes:
    node_id     (int)  : node_id of bus where FlexibleLoads is installed
    number  (int)  : FL object number between all island Flexible Loads
    p_max       (float): Pmax (kW) Installed power # TODO: NO API SUPPORT! CHECK IT (DOES NOT ADDED TO __init__)
    alfa        (float): Alfa (%) Flexibility portion of loads
    lr_pickup   (float): LR_pickup (kW/h) Load pick-up and drop rates
    lr_drop     (float): LR_drop (kW/h) Load pick-up and drop rates
    inc         (float): INC ($/kWh) incentives
    p_fl        (float): output type: set point power for the Flexible Load
    pr_fl       (float): output type: Kwh price
    on          (bool):  output type: indicates activeness of FlexibleLoads
    """

    def __init__(self, node_id: int, number: int, alfa: float, lr_pickup: float, 
        lr_drop: float, inc: float, **kwargs) -> None:
        super().__init__(node_id, number)
        self.alfa = alfa
        self.lr_pickup = lr_pickup
        self.lr_drop = lr_drop
        self.inc = inc
        # outputs:
        self.p_fl = 0
        self.pr_fl = 0
        self.on = True
        # setpoints
        self.sp_p_flex = kwargs.pop('sp_p_flex', {})
        self.sp_q_flex = kwargs.pop('sp_q_flex', {})

    def get_p_fl(self) -> float:
        return self.p_fl

    def get_pr_fl(self) -> float:
        return self.pr_fl

    def get_on(self) -> bool:
        return self.on

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", alpha: " + str(self.alfa) + ", lr_pickup:" \
               + str(self.lr_pickup) + ", lr_drop: " + str(self.lr_drop) + ", inc: " + str(self.inc) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        """creates WF based on FL_source.csv keys and values

        Args:
            item (dict): key, value parameters

        Returns:
            FL: object of FL
        """
        # FL No.,Node_id,Alfa,LR_pickup,LR_drop,INC
        number = item['FL No.']
        node_id = item['Node_id']
        alfa = item['Alfa'] / 100
        lr_pickup = item['LR_pickup']
        lr_drop = item['LR_drop']
        inc = item['INC']

        return FL(node_id=node_id, number=number, alfa=alfa, lr_pickup=lr_pickup, lr_drop=lr_drop, inc=inc)

    def update_params_by_json(self, item: dict) -> None:
        """updates this object based on given item dictionary values

        Args:
            item (dict): key, value structure of the new data
        """
        self.number = item['FL No.']
        self.node_id = item['Node_id']
        self.alfa = item['Alfa'] / 100
        self.lr_pickup = item['LR_pickup']
        self.lr_drop = item['LR_drop']
        self.inc = item['INC']

    def to_dict(self) -> dict:
        """creates a dictionary based on some of the class attributes for the
        purpose of database

        Returns:
            dict: some attributes of the FL with its values
        """
        return self.__dict__

    @staticmethod
    def create_from_dict(_dict: dict):
        """creates a FL based on the given dictionary

        Args:
            _dict (dict): dictionary containing the class attributes and values

        Returns:
            FL: FL object based on given _dict 
        """
        return FL(**_dict)

    def set(self, key: str, value, w: int, t: int):
        """sets the value for the given setpoint

        Args:
            key (str): key of the setpoint
            value ([type]): value of the setpoint
            w (int): w index of the setpoint
            t (int): t index of the setpoint
        """
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 3])

        # active scheduled power of flexible load
        if key == "P_flex":
            if w not in self.sp_p_flex:
                self.sp_p_flex[w] = {}
            self.sp_p_flex[w][t] = value
        # reactive scheduled power of flexible load
        elif key == "Q_flex":
            if w not in self.sp_q_flex:
                self.sp_q_flex[w] = {}
            self.sp_q_flex[w][t] = value
        else:
            raise (KeyError("there is no such key for FL"))

    def get(self, key: str):
        """helper method for reaching the parameter values based on given key

        Args:
            key (str)

        Raises:
            KeyError: raises when the given key is not valid

        Returns:
            [type]: parameter value
        """
        # Incentive payment to flexible loads
        if key == "INC":
            return self.inc
        # Flexibility portion of loads
        if key == "alpha_flex":
            return self.alfa
        # Load pick-up rates
        if key == "LR_pickup":
            return self.lr_pickup
        # Load drop rates
        if key == "LR_drop":
            return self.lr_drop

        raise (KeyError("there is no such key for FL"))
