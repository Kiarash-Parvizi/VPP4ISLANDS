from typing import List
from .Junction import Junction
from .Mapper import Mapper
import socket
from ..PowerResources.DG import DG
from ..PowerResources.ES import ES
from ..PowerResources.PV import PV
from ..PowerResources.FL import FL
from ..PowerResources.WF import WF
from src.PowerResources.FixedLoad import FixedLoad
from ..PowerResources.Resource import Resource
from typing import Type, Set
from src.FakeAPI.OMNIO import OMNIOAPI
from src.PowerResources.LoadCollection import LoadColleciton


class VppBoxNode(Junction):
    # instance variables
    # ip: str
    # port: int
    # endpoint (url): API endpoint
    # node_id
    ###
    def __init__(self, node_id: int, trade_compatible: bool = False, edges: Set[int] = None, ip: str = "",
                 port: int = 0, v_min: float = 11000, v_max: float = 11550, v_rated: float = 11e3, **kwargs) -> None:
        if edges is None:
            edges = set()
        super().__init__(edges)
        self.ip = ip; self.port = port
        self.node_id = node_id

        self.dg_resources = kwargs.pop('dg_resources', Mapper[DG]())
        self.es_resources = kwargs.pop('es_resources', Mapper[ES]())
        self.pv_resources = kwargs.pop('pv_resources', Mapper[PV]())
        self.wf_resources = kwargs.pop('wf_resources', Mapper[WF]())

        if 'load_collection' in kwargs:
            self.load_collection = kwargs['load_collection']
        else:
            self.load_collection = LoadColleciton()
            self.load_collection.fixed_loads.add(FixedLoad(self.node_id))

        # params
        self.v_min = v_min
        self.v_max = v_max
        self.v_rated = v_rated

        # grid node
        self.trade_compatible = trade_compatible

        # set points for grid node
        self.sp_p_da_buy = kwargs.pop('sp_p_da_buy', {})
        self.sp_p_da_sell = kwargs.pop('sp_p_da_sell', {})
        self.sp_q_da_sell = kwargs.pop('sp_q_da_sell', {})
        self.sp_q_da_buy = kwargs.pop('sp_q_da_buy', {})
        self.sp_v = kwargs.pop('sp_v', {})

    def update_data(self) -> None:
        req = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(bin(req))
            data = s.recv(1024)
        ###
        # update here
        ###

    @staticmethod
    def print_resource(resource_map: Mapper) -> None:
        items = resource_map.getItems()
        for item in items:
            print(item[0], " ", type(item[0]), " => ", item[1])

    def __update_resource_by_dic(self, resource_name: str, resource_class: Type[Resource], resource_map: Mapper,
                               data_dic: dict):
        data = data_dic
        number = data[resource_name + ' No.']

        if resource_map.contains(id=number):  # update
            old_item: Resource = resource_map.get(id=number)
            old_item.update_params_by_json(data)

        else:  # add
            resource_map.add_by_id(number, resource_class.get_instance_by_json(data))

    def get(self, key: str):
        if key == "V_min":
            return self.v_min
        if key == "V_max":
            return self.v_max
        if self.trade_compatible:
            if key == "V_Rated":
                return self.v_rated
            else:
                raise KeyError("there is no such key for BoxNode")
        else:
            raise KeyError("there is no such key for BoxNode")

    def set(self, key: str, value, w: int, t: int):
        sp_key = key.split("_")
        key = "_".join(sp_key[2: len(sp_key) - 1])

        if self.trade_compatible:
            # buying power in day-ahead energy market (kW)
            if key == "P_DA_buy":
                if w not in self.sp_p_da_buy:
                    self.sp_p_da_buy[w] = {}
                self.sp_p_da_buy[w][t] = value
            # selling power in day-ahead energy market (kW)
            elif key == "P_DA_sell":
                if w not in self.sp_p_da_sell:
                    self.sp_p_da_sell[w] = {}
                self.sp_p_da_sell[w][t] = value
            elif key == "Q_DA_sell":
                if w not in self.sp_q_da_sell:
                    self.sp_q_da_sell[w] = {}
                self.sp_q_da_sell[w][t] = value
            elif key == "Q_DA_buy":
                if w not in self.sp_q_da_buy:
                    self.sp_q_da_buy[w] = {}
                self.sp_q_da_buy[w][t] = value
            else:
                raise(KeyError(f"there is no such key in BoxNode"))    
        else:
            raise(KeyError("there is no such key in BoxNode"))


    def load_resources_from_api(self) -> None:
        omnio = OMNIOAPI(self.node_id)
        data = omnio.get_resources_data()
        for dt in data:
            if dt['type'] == 'WF':
                self.__update_resource_by_dic("WF", WF, self.wf_resources, dt)
            if dt['type'] == 'ES':
                self.__update_resource_by_dic("ES", ES, self.es_resources, dt)
            if dt['type'] == 'PV':
                self.__update_resource_by_dic("PV", PV, self.pv_resources, dt)
            if dt['type'] == 'DG':
                self.__update_resource_by_dic("DG", DG, self.dg_resources, dt)
            if dt['type'] == 'FL':
                self.__update_resource_by_dic("FL", FL, self.load_collection.flex_loads, dt)

    def to_dict(self) -> dict:
        obj = {}
        obj['_id'] = self.node_id
        obj['node_id'] = self.node_id
        obj['ip'] = self.ip
        obj['port'] = self.port
        # obj['edges'] = self.edges
        obj['dg_resources'] = self.dg_resources.to_dict()
        obj['es_resources'] = self.es_resources.to_dict()        
        obj['pv_resources'] = self.pv_resources.to_dict()
        obj['wf_resources'] = self.wf_resources.to_dict()
        obj['v_min'] = self.v_min
        obj['v_max'] = self.v_max
        obj['v_rated'] = self.v_rated
        obj['load_collection'] = self.load_collection.to_dict()
        obj['trade_compatible'] = self.trade_compatible
        obj['sp_p_da_buy'] = self.sp_p_da_buy
        obj['sp_p_da_sell'] = self.sp_p_da_sell
        obj['sp_q_da_sell'] = self.sp_q_da_sell
        obj['sp_q_da_buy'] = self.sp_q_da_buy
        obj['sp_v'] = self.sp_v
        return obj
    
    @staticmethod
    def create_from_dict(_dict: dict):
        _dict['dg_resources'] = Mapper[DG].create_from_dict(_dict['dg_resources'], DG)
        _dict['es_resources'] = Mapper[ES].create_from_dict(_dict['es_resources'], ES)
        _dict['pv_resources'] = Mapper[PV].create_from_dict(_dict['pv_resources'], PV)
        _dict['wf_resources'] = Mapper[WF].create_from_dict(_dict['wf_resources'], WF)
        _dict['load_collection'] = LoadColleciton.create_from_dict(_dict['load_collection'])
        return VppBoxNode(**_dict)