
class LineProps:
    # instance variables
    # resistance: float -> R (Ohm)
    # capacitance: float -> X (Farad)
    # inductance: float -> i max (A)
    # i_max_pu: float -> i max (p.u)
    ###

    def __init__(self, r, x, i_max, i_max_pu) -> None:
        self.r = r
        self.x = x
        self.i_max = i_max
        self.i_max_pu = i_max_pu

        # setpoings:
        self.i_current = {}

    def calc_powerLoss(self) -> float:
        ### calc power loss here
        return 1.2
        ###

    def get(self, key: str):
        if key == "R":
            return self.r
        if key == "X":
            return self.x
        if key == "Z":
            return self.r**2 + self.x**2
        if key == "I_max":
            return self.i_max
        raise KeyError("there is no such key in LineProps")

    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 3])

        if key == "I":
            if w not in self.i_current:
                self.i_current[w] = {}
            self.i_current[w][t] = value
        else:
            raise KeyError("there is no such key in LineProps")
