from .Resource import Resource


class FL (Resource):
    """Flexible Load class from Resources
    Attributes:
    node_id     (int)  : node_id of bus where FlexibleLoads is installed
    number  (int)  : FL object number between all island Flexible Loads
    alfa        (float): Alfa (%)
    lr_pickup   (float): LR_pickup (kW/h)
    lr_drop     (float): LR_drop (kW/h)
    inc         (float): INC ($/kWh)
    # on          (bool):  indicates activeness of FlexibleLoads
    """

    def __init__(self, node_id: int, number: int, alfa: float, lr_pickup: float, lr_drop: float, inc: float) -> None:
        super().__init__(node_id, number)
        self.alfa = alfa
        self.lr_pickup = lr_pickup
        self.lr_drop = lr_drop
        self.inc = inc

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", alpha: " + str(self.alfa) + ", lr_pickup:" \
               + str(self.lr_pickup) + ", lr_drop: " + str(self.lr_drop) + ", inc: " + str(self.inc) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        # FL No.,Node_id,Alfa,LR_pickup,LR_drop,INC
        number = item['FL No.']
        node_id = item['Node_id']
        alfa = item['Alfa']
        lr_pickup = item['LR_pickup']
        lr_drop = item['LR_drop']
        inc = item['INC']

        return FL(node_id=node_id, number=number, alfa=alfa, lr_pickup=lr_pickup, lr_drop=lr_drop, inc=inc)

    def update_params_by_json(self, item: dict) -> None:
        self.number = item['FL No.']
        self.node_id = item['Node_id']
        self.alfa = item['Alfa']
        self.lr_pickup = item['LR_pickup']
        self.lr_drop = item['LR_drop']
        self.inc = item['INC']
