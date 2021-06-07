from numpy import flexible
from src.PowerResources.FixedLoad import FixedLoad
from src.PowerResources.FL import FL
from src.vppNode.Mapper import Mapper

class LoadColleciton:

    def __init__(self, **kwargs) -> None:
        self.flex_loads = kwargs.pop('flex_loads', Mapper[FL]())
        self.fixed_loads = kwargs.pop('fixed_loads', Mapper[FixedLoad]())

        # setpoints
        self.sp_p_flex = kwargs.pop('sp_p_flex', {})
        self.sp_q_flex = kwargs.pop('sp_q_flex', {})

    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 1])

        # active scheduled power of flexible load (kW)
        if key == "P_S_flex":
            if w not in self.sp_p_flex:
                self.sp_p_flex[w] = {}
            self.sp_p_flex[w][t] = value
        # reactive scheduled power of flexible load (kW)
        elif key == "Q_S_flex":
            if w not in self.sp_q_flex:
                self.sp_q_flex[w] = {}
            self.sp_q_flex[w][t] = value
        else:
            raise (KeyError("there is no such key for FL"))
    
    def get(self, key: str):
        # Incentive payment to flexible loads ($/kWh)
        if key == "INC_S":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("INC")
            else:
                return 0
        
        # Flexibility portion of loads (%)
        if key == "alpha_S_flex":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("alpha_flex")
            else:
                return 0
        
        # Load pick-up rates (kW/h)
        if key == "LR_S_pickup":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("LR_pickup")
            else:
                return 0
        
        # Load drop rates (kW/h)
        if key == "LR_S_drop":
            if self.flex_loads.len() is not 0:
                return next(iter(self.flex_loads.getItems()))[1].get("LR_drop")
            else:
                return 0
        # Sum of Active loads (kW)
        if key == "P_S_L":
            return next(iter(self.fixed_loads.getItems()))[1].get("P_L")
        
        # Sum of Reactivate Loads (kW)
        if key == "Q_S_L":
            return next(iter(self.fixed_loads.getItems()))[1].get("Q_L")
        
        raise (KeyError("there is no such key for FL"))
    
    def to_dict(self) -> dict:
        obj = {}
        obj['sp_p_flex'] = self.sp_p_flex
        obj['sp_q_flex'] = self.sp_q_flex
        obj['flex_loads'] = self.flex_loads.to_dict()
        obj['fixed_loads'] = self.fixed_loads.to_dict()
        return obj
    
    @staticmethod
    def create_from_dict(_dict: dict):
        obj = LoadColleciton()
        obj.sp_q_flex = _dict['sp_q_flex']
        obj.sp_p_flex = _dict['sp_p_flex']
        obj.flex_loads = Mapper[FL]().create_from_dict(_dict['flex_loads'], FL)
        obj.fixed_loads = Mapper[FixedLoad]().create_from_dict(_dict['fixed_loads'], FixedLoad)
        return obj