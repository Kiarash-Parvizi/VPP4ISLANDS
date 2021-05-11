from .Resource import Resource


class ES(Resource):
    """Energy Storage class from Resources
    Attributes:
    node_id         (int)  : node_id of bus where ES is installed
    number  (int)  : ES object number between all island Energy Storages
    p_max_charge    (float): p_charge in kW maximum charging power
    p_max_discharge (float): p_discharge in kW maximum discharging power
    energy_capacity (float): Energy Capacity in kWh
    soe_min         (float): percentage of SEO min
    soe_max         (float): percentage of SEO max
    # efficiency      (float): Efficiency in percentage
    efficiency_charge  (float): Efficiency charge
    efficiency_discharge (float): by default equal to Efficiency_charge, unless a different value is given
    soe_initial     (float): SOE_initial in percentage
    p_ess           (float): output type: set point power for the ess
    pr_ess          (float): output type: Kwh price
    """

    def __init__(self, node_id: int, number: int, p_max_charge: float, p_max_discharge: float, energy_capacity: float,
                 soe_min: float, soe_max: float, efficiency_charge: float, efficiency_discharge: float,
                 soe_initial: float) -> None:
        super().__init__(node_id, number)
        self.p_max_charge = p_max_charge
        self.p_max_discharge = p_max_discharge
        self.energy_capacity = energy_capacity
        self.soe_min = soe_min
        self.soe_max = soe_max
        # self.efficiency = efficiency
        self.efficiency_charge = efficiency_charge
        self.efficiency_discharge = efficiency_discharge
        self.soe_initial = soe_initial
        # outputs
        self.p_ess = 0
        self.pr_ess = 0
        # setpoints
        self.sp_p_ch_es = {}
        self.sp_p_dch_es = {}
        self.sp_soe_es = {}

    def get_p_ess(self) -> float:
        return self.p_ess

    def get_pr_ess(self) -> float:
        return self.pr_ess

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", p_max_charge: " + str(self.p_max_charge) + \
               ", p_max_discharge: " + str(self.p_max_discharge) + ", energy_capacity: " + str(self.energy_capacity) + \
               ", soe_min: " + str(self.soe_min) + ", soe_max: " + str(self.soe_max) + ", efficiency_charge: " + str(
            self.efficiency_charge) + ", efficiency_discharge: " + str(self.efficiency_discharge) + ", soe_initial: "\
               + str(self.soe_initial) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        number = item['ES No.']
        node_id = item['Node_id']
        p_max_charge = item['P_charge']
        p_max_discharge = item['P_discharge']
        energy_capacity = item['Energy Capacity']
        soe_min = item['SOE_min']
        soe_max = item['SOE_max']
        efficiency = item['Efficiency']
        soe_initial = item['SOE_initial']

        return ES(node_id=node_id, number=number, p_max_charge=p_max_charge, p_max_discharge=p_max_discharge,
                  energy_capacity=energy_capacity, soe_min=soe_min, soe_max=soe_max, efficiency_charge=efficiency,
                  efficiency_discharge=efficiency, soe_initial=soe_initial)

    def update_params_by_json(self, item: dict) -> None:
        self.number = item['ES No.']
        self.node_id = item['Node_id']
        self.p_max_charge = item['P_charge']
        self.p_max_discharge = item['P_discharge']
        self.energy_capacity = item['Energy Capacity']
        self.soe_min = item['SOE_min']
        self.soe_max = item['SOE_max']
        self.efficiency_charge = item['Efficiency']
        self.efficiency_discharge = item['Efficiency']
        self.soe_initial = item['SOE_initial']

    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        return ES(**_dict)
    
    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 3])

        # Scheduled Charge Power of ESs
        if key == "P_ChES":
            if w not in self.sp_p_ch_es:
                self.sp_p_ch_es[w] = {}
            self.sp_p_ch_es[w][t] = value
        # Scheduled Discharge Power of ESs
        elif key == "P_DchES":
            if w not in self.sp_p_dch_es:
                self.sp_p_dch_es[w] = {}
            self.sp_p_dch_es[w][t] = value
        # State of the energy level of ESs
        elif key == "SOE_ES":
            if w not in self.sp_soe_es:
                self.sp_soe_es[w] = {}
            self.sp_soe_es[w][t] = value
        else:
            raise(KeyError("there is no such key for ES"))

    def get(self, key: str):
        # Maximum charge power of energy storages
        if key == "P_ChES_max":
            return self.p_max_charge
        # Maximum discharge power of energy storages
        if key == "P_DchES_max":
            return self.p_max_discharge
        # Charge efficiency of energy storages
        if key == "eta_ChES":
            return self.efficiency_charge
        # Discharge efficiency of energy storages
        if key == "eta_DchES":
            return self.efficiency_discharge
        # Minimum state of energy level of energy storages
        if key == "SOE_ES_min":
            return self.soe_min
        # Maximum state of energy level of energy storages
        if key == "SOE_ES_max":
            return self.soe_max
        raise(KeyError("there is no such key in ES"))
       