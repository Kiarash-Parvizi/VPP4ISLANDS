
class LineProps:
    # instance variables
    # length: float
    # resistance: float
    # capacitance: float
    # inductance: float
    ###

    def __init__(self, length, resistance, capacitance, inductance) -> None:
        self.length = length
        self.resistance  = resistance
        self.capacitance = capacitance
        self.inductance  = inductance

    def calc_powerLoss() -> float:
        ### calc power loss here
        return 1.2
        ###

