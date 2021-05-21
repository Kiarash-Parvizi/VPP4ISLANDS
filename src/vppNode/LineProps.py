
class LineProps:
    # instance variables
    # resistance: float -> R (Ohm)
    # capacitance: float -> X (Farad)
    # inductance: float -> i max (A)
    # i_max_pu: float -> i max (p.u)
    ###

    def __init__(self, resistance, capacitance, inductance, i_max_pu) -> None:
        self.resistance = resistance
        self.capacitance = capacitance
        self.inductance = inductance
        self.i_max_pu = i_max_pu

    def calc_powerLoss(self) -> float:
        ### calc power loss here
        return 1.2
        ###

