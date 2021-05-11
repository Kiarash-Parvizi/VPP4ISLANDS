from .Resource import Resource


class DG(Resource):
    """Distributed Generators class from Resources
    Attributes:
    node_id (int)  : node_id of bus where DG is installed
    number  (int)  : DG object number between all island Distributed Generators
    p_max   (float): p_max (kW)
    p_min   (float): p_min (kW)
    q_max   (float): Q_max (kW)
    q_min   (float): Q_min (kW)
    rup     (float): Rup (kW/h)
    rdn     (float): Rdn (kW/h)
    mut     (float): MUT (h)
    mdt     (float): MDT (h)
    cost    (float): Cost ($/kWh)
    suc     (float): SUC ($)
    sdc     (float): SDC ($)
    p_dg    (float): output type: set point power for the DG
    pr_dg   (float): output type: Kwh price
    on      (boolean): output type: true to work, false to stop working
    """

    def __init__(self, node_id: int, number: int, p_max: float, p_min: float, q_max: float, q_min: float, rup: float,
                 rdn: float, mut: float, mdt: float, cost: float, suc: float, sdc: float) -> None:
        super().__init__(node_id, number)
        self.p_max = p_max
        self.p_min = p_min
        self.q_max = q_max
        self.q_min = q_min
        self.rup = rup
        self.rdn = rdn
        self.mut = mut
        self.mdt = mdt
        self.cost = cost
        self.suc = suc
        self.sdc = sdc
        # outputs
        self.p_dg = 0
        self.pr_dg = 0
        self.on = True

    def get_p_dg(self) -> float:
        return self.p_dg

    def get_pr_dg(self) -> float:
        return self.pr_dg

    def get_on(self) -> bool:
        return self.on

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", p_max: " + str(self.p_max) + ", p_min: " + \
               str(self.p_min) + ", q_max: " + str(
            self.q_max) + ", q_min: " + str(self.q_min) + ", rup: " + str(self.rup) + ", rdn: " + \
               str(self.rdn) + ", mut: " + str(self.mut) + ", mdt: " + str(self.mdt) + ", cost: " + str(self.cost) + \
               ", suc: " + str(self.suc) + ", sdc: " + str(self.sdc) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        # DG No.,Node_id,P_max,P_min,Q_max,Q_min,Rup,Rdn,MUT,MDT,Cost,SUC,SDC
        number = item['DG No.']
        node_id = item['Node_id']
        p_max = item['P_max']
        p_min = item['P_min']
        q_max = item['Q_max']
        q_min = item['Q_min']
        rup = item['Rup']
        rdn = item['Rdn']
        mut = item['MUT']
        mdt = item['MDT']
        cost = item['Cost']
        suc = item['SUC']
        sdc = item['SDC']

        return DG(node_id=node_id, number=number, p_max=p_max, p_min=p_min, q_max=q_max, q_min=q_min, rup=rup,
                  rdn=rdn, mut=mut, mdt=mdt, cost=cost, suc=suc, sdc=sdc)

    def update_params_by_json(self, item: dict):
        self.number = item['DG No.']
        self.node_id = item['Node_id']
        self.p_max = item['P_max']
        self.p_min = item['P_min']
        self.q_max = item['Q_max']
        self.q_min = item['Q_min']
        self.rup = item['Rup']
        self.rdn = item['Rdn']
        self.mut = item['MUT']
        self.mdt = item['MDT']
        self.cost = item['Cost']
        self.suc = item['SUC']
        self.sdc = item['SDC']

    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        return DG(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        pass
    
    def get(self, key: str):
        pass