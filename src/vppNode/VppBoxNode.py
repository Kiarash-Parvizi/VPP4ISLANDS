from typing import List
from .Junction import Junction
from .Mapper import Mapper
import socket
import requests
from PowerResources.DG import DG
from PowerResources.ES import ES
from PowerResources.PV import PV
from PowerResources.FL import FL
from PowerResources.WF import WF
from PowerResources.Resource import Resource
from typing import Type


class VppBoxNode(Junction):
    # instance variables
    # ip: str
    # port: int
    # endpoint (url): API endpoint
    ###
    def __init__(self, edges: List[int] = [], ip: str = "", port: int = 0) -> None:
        super().__init__(edges)
        self.ip = ip; self.port = port
        # TODO: change the endpoint to what OMNIO provides
        self.endpoint = "http://localhost:8000"
        self.dg_resources = Mapper[DG]()
        self.es_resources = Mapper[ES]()
        self.fl_resources = Mapper[FL]()
        self.pv_resources = Mapper[PV]()
        self.wf_resources = Mapper[WF]()
    
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

    def update_resource(self, resource_name: str, resource_class: Type[Resource], resource_map: Mapper):
        res: dict = requests.get(self.endpoint + "/" + resource_name).json()
        data = res['data']
        for item in data:
            number = item[resource_name + ' No.']

            if resource_map.contains(id=number):  # update
                old_item: Resource = resource_map.get(id=number)
                old_item.update_params_by_json(item)

            else:  # add
                resource_map.add_by_id(number, resource_class.get_instance_by_json(item))

    def update_resources(self) -> None:
        self.update_resource("ES", ES, self.es_resources)
        self.update_resource("WF", WF, self.wf_resources)
        self.update_resource("PV", PV, self.pv_resources)
        self.update_resource("DG", DG, self.dg_resources)
        self.update_resource("FL", FL, self.fl_resources)

    @staticmethod
    def print_resource(resource_map: Mapper) -> None:
        items = resource_map.getItems()
        for item in items:
            print(item[0], " => ", item[1])
