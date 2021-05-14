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
from typing import Type
from src.FakeAPI.OMNIO import OMNIOAPI


class VppBoxNode(Junction):
    # instance variables
    # ip: str
    # port: int
    # endpoint (url): API endpoint
    # node_id
    ###
    def __init__(self, node_id: int, p_max: float = 0, i_max: float = 0, edges: List[int] = [], ip: str = "", \
                 port: int = 0) -> None:
        super().__init__(edges)
        self.ip = ip; self.port = port
        self.node_id = node_id
        # TODO: change the endpoint to what OMNIO provides
        self.endpoint = "http://localhost:8001"
        self.dg_resources = Mapper[DG]()
        self.es_resources = Mapper[ES]()
        self.fl_resources = Mapper[FL]()
        self.pv_resources = Mapper[PV]()
        self.wf_resources = Mapper[WF]()
        self.fixed_load = FixedLoad(self.node_id)
        # self.flexible_load = 0
        # self.fixed_load = 0
        self.p_max = p_max
        self.i_max = i_max

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
            print(item[0], " => ", item[1])

    def __update_resource_by_dic(self, resource_name: str, resource_class: Type[Resource], resource_map: Mapper,
                               data_dic: dict):
        data = data_dic
        number = data[resource_name + ' No.']

        if resource_map.contains(id=number):  # update
            old_item: Resource = resource_map.get(id=number)
            old_item.update_params_by_json(data)

        else:  # add
            resource_map.add_by_id(number, resource_class.get_instance_by_json(data))

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
                self.__update_resource_by_dic("FL", FL, self.fl_resources, dt)

    def to_dict(self) -> dict:
        obj = {}
        obj['_id'] = self.node_id
        obj['node_id'] = self.node_id
        # obj['flexible_load'] = self.flexible_load
        # obj['fixed_load'] = self.fixed_load
        obj['p_max'] = self.p_max
        obj['i_max'] = self.i_max
        obj['ip'] = self.ip
        obj['port'] = self.port
        obj['endpoint'] = self.endpoint
        obj['edges'] = self.edges
        return obj
    
    @staticmethod
    def create_from_dict(self, _dict: dict):
        return VppBoxNode(**_dict)