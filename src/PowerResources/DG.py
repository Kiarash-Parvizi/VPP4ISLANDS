from .Resource import Resource


class DG(Resource):
    """Distributed Generators class from Resources
    Attributes:
    node_id (int)  : node_id of bus where DG is installed
    number  (int)  : DG object number between all island Distributed Generators
    p_max   (float): p_max (kW) maximum installed power
    p_min   (float): p_min (kW) Minimum power
    q_max   (float): Q_max (kW) maximum reactive power
    q_min   (float): Q_min (kW) Minimum reactive power
    rup     (float): Rup (kW/h) Ramp up rates of DGs
    rdn     (float): Rdn (kW/h) Ramp down rates of DGs
    mut     (float): MUT (h) Minimum up times of DGs
    mdt     (float): MDT (h) Minimum down times of DGs
    cost    (float): Cost ($/kWh) Generation cost of DGs
    suc     (float): SUC ($) Start-up/shut-down costs of conventional DGs
    sdc     (float): SDC ($) Start-up/shut-down costs of conventional DGs
    p_dg    (float): output type: set point power for the DG
    pr_dg   (float): output type: Kwh price
    on      (boolean): output type: true to work, false to stop working
    """

    def __init__(self, node_id: int, number: int, p_max: float, p_min: float, q_max: float, q_min: float, rup: float,
                 rdn: float, mut: float, mdt: float, cost: float, suc: float, sdc: float, **kwargs) -> None:
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
        # setpoints
        self.sp_p_dg = kwargs.pop('sp_p_dg', {})
        self.sp_q_dg = kwargs.pop('sp_q_dg', {})
        self.sp_v_dg_su = kwargs.pop('sp_v_dg_su', {})
        self.sp_v_dg_sd = kwargs.pop('sp_v_dg_sd', {})
        self.sp_u_dg = kwargs.pop('sp_u_dg', {})

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
        """creates DG based on DG_source.csv keys and values

        Args:
            item (dict): key, value parameters

        Returns:
            DG: object of DG
        """
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
        """updates this object based on given item dictionary values

        Args:
            item (dict): key, value structure of the new data
        """
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
        """creates a dictionary based on some of the class attributes for the
        purpose of database

        Returns:
            dict: some attributes of the DG with its values
        """
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        """creates a DG based on the given dictionary

        Args:
            _dict (dict): dictionary containing the class attributes and values

        Returns:
            DG: DG object based on given _dict 
        """
        return DG(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        """sets the value for the given setpoint

        Args:
            key (str): key of the setpoint
            value ([type]): value of the setpoint
            w (int): w index of the setpoint
            t (int): t index of the setpoint
        """
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 2])

        # Active output power of DG units (kW)
        if key == "P_DG":
            if w not in self.sp_p_dg:
                self.sp_p_dg[w] = {}
            self.sp_p_dg[w][t] = value
        # Reactive output power of DG units (kW)
        elif key == "Q_DG":
            if w not in self.sp_q_dg:
                self.sp_q_dg[w] = {}
            self.sp_q_dg[w][t] = value
        # Start-up binary variables of DG units (1/0)
        elif key == "v_DG_SU":
            if w not in self.sp_v_dg_su:
                self.sp_v_dg_su[w] = {}
            self.sp_v_dg_su[w][t] = value
        # shut-down binary variables of DG units (1/0)
        elif key == "v_DG_SD":
            if w not in self.sp_v_dg_sd:
                self.sp_v_dg_sd[w] = {}
            self.sp_v_dg_sd[w][t] = value
        # Binary variable indicates on/off situation of DG units (1/0)
        elif key == "U_DG":
            if w not in self.sp_u_dg:
                self.sp_u_dg[w] = {}
            self.sp_u_dg[w][t] = value
        else:
            raise(KeyError("there is no such key for DG"))

    def get(self, key: str):
        """helper method for reaching the parameter values based on given key

        Args:
            key (str)

        Raises:
            KeyError: raises when the given key is not valid

        Returns:
            [type]: parameter value
        """
        # start-up costs of conventional DGs ($)
        if key == "SUC_DG":
            return self.suc
        # shut-down costs of conventional DGs ($)
        if key == "SDC_DG":
            return self.sdc
        # Generation cost of DGs ($/kWh)
        if key == "C_DG":
            return self.cost
        # Minimum active power of DGs (kW)
        if key == "P_DG_min":
            return self.p_min
        # Maximum active power of DGs (kW)
        if key == "P_DG_max":
            return self.p_max
        # Minimum reactive power of DGs (kW)
        if key == "Q_DG_min":
            return self.q_min
        # Maximum reactive power of DGs (kW)
        if key == "Q_DG_max":
            return self.q_max
        # Ramp up rates of DGs (kW/h)
        if key == "RU_DG":
            return self.rup
        # Ramp down rates of DGs (kW/h)
        if key == "RD_DG":
            return self.rdn
        # Minimum up times of DGs (h)
        if key == "MUT":
            return self.mut
        # Minimum down times of DGs (h)
        if key == "MDT":
            return self.mdt
        raise(KeyError("there is no such key for DG"))