from numpy import flexible
from src.PowerResources.FixedLoad import FixedLoad
from src.PowerResources.FL import FL
from src.vppNode.Mapper import Mapper

class LoadColleciton:

    def __init__(self) -> None:
        self.flex_loads = Mapper[FL]()
        self.fixed_loads = Mapper[FixedLoad]()

        # setpoints
        self.sp_p_flex = {}
        self.sp_q_flex = {}

    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 1])

        # active scheduled power of flexible load
        if key == "P_S_flex":
            if w not in self.sp_p_flex:
                self.sp_p_flex[w] = {}
            self.sp_p_flex[w][t] = value
        # reactive scheduled power of flexible load
        elif key == "Q_S_flex":
            if w not in self.sp_q_flex:
                self.sp_q_flex[w] = {}
            self.sp_q_flex[w][t] = value
        else:
            raise (KeyError("there is no such key for FL"))
    
    def get(self, key: str):
        # Incentive payment to flexible loads
        if key == "INC_S":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("INC")
            else:
                return 0
        
        # Flexibility portion of loads
        if key == "alpha_S_flex":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("alpha_flex") / 100.
            else:
                return 0
        
        # Load pick-up rates
        if key == "LR_S_pickup":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("LR_pickup")
            else:
                return 0
        
        # Load drop rates
        if key == "LR_S_drop":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("LR_drop")
            else:
                return 0
        
        if key == "P_S_L":
            return next(iter(self.fixed_loads.getItems()))[1].get("P_L")
        
        if key == "Q_S_L":
            return next(iter(self.fixed_loads.getItems()))[1].get("Q_L")
        
        raise (KeyError("there is no such key for FL"))