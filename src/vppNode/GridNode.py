from .Junction import Junction

class GridNode(Junction):
    # instance variables
    # write the name of your vars here
    ###
    def __init__(self) -> None:
        # setpoints
        self.sp_p_da_buy = {}
        self.sp_p_da_sell = {}
    
    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 3])

        # buying power in day-ahead energy market
        if key == "P_DA_buy":
            if w not in self.sp_p_da_buy:
                self.sp_p_da_buy[w] = {}
            self.sp_p_da_buy[w][t] = value
        # selling power in day-ahead energy market
        elif key == "P_DA_sell":
            if w not in self.sp_p_da_sell:
                self.sp_p_da_sell[w] = {}
            self.sp_p_da_sell[w][t] = value
        else:
            raise(KeyError("there is no such key in GridNode"))
    
    def get(self, key: str):
        pass