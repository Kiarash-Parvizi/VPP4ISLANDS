import requests
from src.FakeAPI.utils import read_node_data

class OMNIOAPI:
    """OMNIO API CONNECTOR
    """
    def __init__(self, node_id: int) -> None:
        self.endpoint = "http://localhost:8001"
        self.node_id = node_id
    
    def get_resources_data(self) -> dict:
        # res = requests.get(self.endpoint + "/node-resources/" + str(
        #     self.node_id)).json()
        # data = res['data']
        data = read_node_data(self.node_id)['data']
        return data
