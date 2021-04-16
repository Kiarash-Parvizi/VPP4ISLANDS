from .Resource import Resource


class ES(Resource):
    """Energy Storage class from Resources
    Attributes:
    node_id         (int)  : node_id of bus where ES is installed
    number  (int)  : ES object number between all island Energy Storages
    p_charge        (float): p_charge in kW
    p_discharge     (float): p_discharge in kW
    energy_capacity (float): Energy Capacity in kWh
    soe_min         (float): percentage of SEO min
    soe_max         (float): percentage of SEO max
    efficiency      (float): Efficiency in percentage
    soe_initial     (float): SOE_initial in percentage
    """

    def __init__(self, node_id: int, number: int, p_charge: float, p_discharge: float, energy_capacity: float,
                 soe_min: float, soe_max: float, efficiency: float, soe_initial: float) -> None:
        super().__init__(node_id, number)
        self.p_charge = p_charge
        self.p_discharge = p_discharge
        self.energy_capacity = energy_capacity
        self.soe_min = soe_min
        self.soe_max = soe_max
        self.efficiency = efficiency
        self.soe_initial = soe_initial

    def __str__(self) -> str:
        return self.__class__.__name__ + " : { " + super().__str__() + ", p_charge: " + str(self.p_charge) + \
               ", p_discharge: " + str(self.p_discharge) + ", energy_capacity: " + str(self.energy_capacity) + \
               ", soe_min: " + str(self.soe_min) + ", soe_max: " + str(self.soe_max) + ", efficiency: " + str(
            self.efficiency) + ", soe_initial: " + str(self.soe_initial) + " }"

    @staticmethod
    def get_instance_by_json(item: dict):
        number = item['ES No.']
        node_id = item['Node_id']
        p_charge = item['P_charge']
        p_discharge = item['P_discharge']
        energy_capacity = item['Energy Capacity']
        soe_min = item['SOE_min']
        soe_max = item['SOE_max']
        efficiency = item['Efficiency']
        soe_initial = item['SOE_initial']

        return ES(node_id=node_id, number=number, p_charge=p_charge, p_discharge=p_discharge,
                  energy_capacity=energy_capacity, soe_min=soe_min, soe_max=soe_max, efficiency=efficiency,
                  soe_initial=soe_initial)

    def update_params_by_json(self, item: dict) -> None:
        self.number = item['ES No.']
        self.node_id = item['Node_id']
        self.p_charge = item['P_charge']
        self.p_discharge = item['P_discharge']
        self.energy_capacity = item['Energy Capacity']
        self.soe_min = item['SOE_min']
        self.soe_max = item['SOE_max']
        self.efficiency = item['Efficiency']
        self.soe_initial = item['SOE_initial']
