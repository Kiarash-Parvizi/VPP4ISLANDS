from abc import abstractmethod


class Resource:
    """Resource class
    Attributes:
    node_id (int): id of nodes which the resource is installed.
    number  (int)  : Resource object number between all island Resources
    """
    def __init__(self, node_id: int, number: int) -> None:
        self.node_id = node_id
        self.number = number
        self.sbase = 23e5

    def __str__(self) -> str:
        return "node_id: " + str(self.node_id) + ", number: " + str(self.number)

    @abstractmethod
    def update_params_by_json(self, item: dict):
        pass

    @staticmethod
    @abstractmethod
    def get_instance_by_json(item: dict):
        pass

    def to_dict(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def create_from_dict(_dict: dict):
        return Resource(**_dict)