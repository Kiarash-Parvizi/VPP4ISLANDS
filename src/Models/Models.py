from src.Models.Database import DBClient
from src.vppNode.VppBoxNode import VppBoxNode
from src.vppNode.VppNode import VppNode
from src.PowerResources.DG import DG
from src.PowerResources.PV import PV
from src.PowerResources.ES import ES
from src.PowerResources.FL import FL
from src.PowerResources.WF import WF
import json
from datetime import datetime

class BoxNodesModel:
    """A VppBoxNode mongodb database Schema
    """
    def __init__(self) -> None:
        self.client = DBClient()
        self.database_name = "VPPNode"
        self.collection_name = "BoxNodes"
        self.col = self.client.get_collection(
            database_name=self.database_name, collection_name=self.collection_name)



    def insert_boxnode(self, box_node: VppBoxNode) -> bool:
        """inserts the given VppBoxNode to the corresponding database and 
        collection.

        Args:
            box_node (VppBoxNode): a VppBoxNode object

        Returns:
            bool: True if the insertion was successfully done
        """
        _query = {"_id" : box_node.node_id}
        found_obj = self.col.find_one(_query)
        # res = self.col.find_one_and_update(_query, {"$set": box_node.to_dict()}, upsert=True)
        if found_obj:
            print(f"node {box_node.node_id} already exists")
        else:
            json_data = json.dumps(box_node.to_dict())
            _dict = json.loads(json_data)
            res = self.col.insert_one(_dict)
        return True
    
    def update_boxnode(self, box_node: VppBoxNode) -> bool:
        """updates the given VppBoxNode to the corresponding database and 
        collection.

        Args:
            box_node (VppBoxNode): a VppBoxNode object

        Returns:
            bool: True if the update was successfully done
        """
        _query = {"_id" : box_node.node_id}
        res = self.col.find_one_and_update(_query, {"$set": box_node.to_dict()}, upsert=True)
        print(res)
        return True
    
    def get_boxnode_by_id(self, _id: int) -> VppBoxNode:
        """returns VppBoxNode based on given _id

        Args:
            _id (int): id

        Returns:
            VppBoxNode: an object of VppBoxNode
        """
        _query = {"_id" : _id}
        res = self.col.find_one(_query)
        box_node = None
        if res:
            box_node = VppBoxNode.create_from_dict(res)
        return box_node
    
    def add_one_dg_by_id(self, _id: int, dg: DG):
        """adds a DG object to the data base (just a test)

        Args:
            _id (int): id
            dg (DG): an object of DG
        """
        _query = {"_id" : _id}
        res = self.col.update_one(_query, {"$push", {'dgs' : dg.to_dict()}}, upsert=True)
        print(res)

class VppNodeModel:
    """A VppNode mongodb database Schema
    """
    def __init__(self) -> None:
        self.client = DBClient()
        self.database_name = "VPPNode"
        self.collection_name = "VppNodes"
        self.col = self.client.get_collection(
            database_name=self.database_name, collection_name=self.collection_name)
    
    def insert_vppnode(self, vpp_node: VppNode) -> bool:
        """inserts the given VppNode to the database with a timestamp.

        Args:
            vpp_node (VppNode): a VppNode object

        Returns:
            bool: True if the insertion was successfully done.
        """
        _dict = json.loads(json.dumps(vpp_node.to_dict()))
        _dict['time'] = datetime.now()
        res = self.col.insert_one(_dict)
        return True
