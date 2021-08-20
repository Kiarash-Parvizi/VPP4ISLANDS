from typing import Tuple
import math

class LineProps:
    # instance variables
    # resistance: float -> R (Ohm)
    # capacitance: float -> X (Farad)
    # inductance: float -> i max (A)
    # i_max_pu: float -> i max (p.u)
    ###

    def __init__(self, r: float, x: float, i_max: float, i_max_pu: float, **kwargs) -> None:
        self.r = r
        self.x = x
        self.i_max = i_max
        self.i_max_pu = i_max_pu
        self.dir_data = {
            'P_+': {},
            'P_-': {},
            'Q_+': {},
            'Q_-': {},
        } # data about directed edge

        # setpoings:
        self.i_current = kwargs.pop('i_current', {})

    def calc_powerLoss(self) -> float:
        ### calc power loss here
        return 1.2
        ###

    def get(self, key: str):
        """helper method for reaching the parameter values based on given key

        Args:
            key (str)

        Raises:
            KeyError: raises when the given key is not valid

        Returns:
            [Any]: parameter value
        """
        if key == "R":
            return self.r
        if key == "X":
            return self.x
        if key == "Z":
            return math.sqrt(self.r**2 + self.x**2)
        if key == "I_max":
            return self.i_max
        raise KeyError("there is no such key in LineProps")

    def set(self, key: str, value, w: int, t: int):
        """sets the value for the given setpoint

        Args:
            key (str): key of the setpoint
            value ([type]): value of the setpoint
            w (int): w index of the setpoint
            t (int): t index of the setpoint
        """
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 3])

        if key == "I":
            if w not in self.i_current:
                self.i_current[w] = {}
            self.i_current[w][t] = value
        else:
            raise KeyError("there is no such key in LineProps")

    def to_dict(self):
        """creates a dictionary based on some of the class attributes for the
        purpose of database

        Returns:
            dict: some attributes of the LineProps with its values
        """
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        """creates a LineProps based on the given dictionary

        Args:
            _dict (dict): dictionary containing the class attributes and values

        Returns:
            LineProps: LineProps object based on given _dict 
        """
        return LineProps(**_dict)
    
    def set_dir_data(self, key: str, value, DEdge: Tuple[int, int], w: int, t: int):
        """sets values having direction for the given setpoints

        Args:
            key (str): the given key
            value ([type]): the given value
            DEdge (Tuple[int, int]): tuple indicated the direction
            w (int): w index
            t (int): time index

        Raises:
            KeyError: raises when there is no such key in LineProps::dir_data
        """
        # just for test
        #if not hasattr(self, 'cnt'):
        #    self.cnt = 0
        #self.cnt += 1
        #if self.cnt == 192:
        #    import pprint
        #    pprint.pprint(self.dir_data)
        #print('cnt: ', self.cnt)
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 2])
        DEdge = str(DEdge)

        if not key in self.dir_data:
            raise KeyError("there is no such key in LineProps::dir_data")
        
        if DEdge not in self.dir_data[key]:
            self.dir_data[key][DEdge] = {}

        ddat = self.dir_data[key][DEdge]
        if w not in ddat:
            ddat[w] = {}
        ddat[w][t] = value
