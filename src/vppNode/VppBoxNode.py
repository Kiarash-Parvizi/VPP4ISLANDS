from typing import List
from .Junction import Junction
from .Mapper import Mapper
import socket
import requests
from ..PowerResources.DG import DG
from ..PowerResources.ES import ES
from ..PowerResources.PV import PV
from ..PowerResources.FL import FL
from ..PowerResources.WF import WF
from ..PowerResources.Resource import Resource
from typing import Type
from .UncertaintyParams import UncertaintyParams


class VppBoxNode(Junction):
    # instance variables
    # ip: str
    # port: int
    # endpoint (url): API endpoint
    # node_id
    ###
    def __init__(self, node_id: int, edges: List[int] = [], ip: str = "", port: int = 0) -> None:
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
        self.flexible_load = 0
        self.fixed_load = 0

    def update_data(self) -> None:
        req = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(bin(req))
            data = s.recv(1024)
        ###
        # update here
        ###

    def get_load_data(self) -> None:
        # TODO: delete this method, it's not VPPBox business
        response = requests.get(self.endpoint + "/load-data")
        data = response.json()
        print(data)

    def get_uncertainty_params(self, time: int) -> None:
        res = requests.get(self.endpoint + "/uncertainty-params/" + str(time)).json()
        uncertainty_params = UncertaintyParams.get_instance_by_json(res['data'])
        return uncertainty_params

    @staticmethod
    def print_resource(resource_map: Mapper) -> None:
        items = resource_map.getItems()
        for item in items:
            print(item[0], " => ", item[1])

    def update_resource_by_dic(self, resource_name: str, resource_class: Type[Resource], resource_map: Mapper,
                               data_dic: dict):
        data = data_dic
        number = data[resource_name + ' No.']

        if resource_map.contains(id=number):  # update
            old_item: Resource = resource_map.get(id=number)
            old_item.update_params_by_json(data)

        else:  # add
            resource_map.add_by_id(number, resource_class.get_instance_by_json(data))

    def get_resource_data(self) -> None:
        res = requests.get(self.endpoint + "/node-resources/" + str(self.node_id)).json()
        data = res['data']
        for dt in data:
            if dt['type'] == 'WF':
                self.update_resource_by_dic("WF", WF, self.wf_resources, dt)
            if dt['type'] == 'ES':
                self.update_resource_by_dic("ES", ES, self.es_resources, dt)
            if dt['type'] == 'PV':
                self.update_resource_by_dic("PV", PV, self.pv_resources, dt)
            if dt['type'] == 'DG':
                self.update_resource_by_dic("DG", DG, self.dg_resources, dt)
            if dt['type'] == 'FL':
                self.update_resource_by_dic("FL", FL, self.fl_resources, dt)

    def get_flexible_load(self, time: int):
        res = res = requests.get(self.endpoint + "/node-flexible-load/" + str(self.node_id) + f"?time={time}").json()
        data = res['data']
        if res['status'] != 404:
            self.flexible_load = data['load']

    def get_fixed_load(self, time: int):
        res = res = requests.get(self.endpoint + "/node-fixed-load/" + str(self.node_id) + f"?time={time}").json()
        data = res['data']
        if res['status'] != 404:
            self.fixed_load = data['load']
