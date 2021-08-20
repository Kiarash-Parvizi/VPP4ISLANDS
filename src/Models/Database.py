from pymongo import MongoClient
from typing import Any
import json

class Singleton(type):
    """Singletone helper class
    """
    _instance = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self not in self._instance:
            self._instance[self] = super(Singleton, self).__call__(*args, **kwds)
            return self._instance[self]

class DBSettings(metaclass=Singleton):
    """DBSetting class, contains username, password, ip, port and a connector
    to the database. Above attributes are available in the given dir_config path.

    Args:
        metaclass ([type], optional): Defaults to Singleton.
    """
    def __init__(self, dir_config: str) -> None:
        data = None
        with open(dir_config) as f:
            data = json.load(f)
        self.username = data['database']['username']
        self.password = data['database']['password']
        self.host = data['database']['host']
        self.port = data['database']['port']
        self.connector_host = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"

class DBClient(metaclass=Singleton):
    """A Database client class for connecting to the database

    Args:
        metaclass ([type], optional): Defaults to Singleton.
    """
    def __init__(self) -> None:
        self.settings = DBSettings("./config/config.json")
        self.mongoClient = MongoClient(
            host=self.settings.connector_host, port=self.settings.port)

    def get_database_names(self) -> list:
        """returns all the available mongodb databases.

        Returns:
            list: list of databases name
        """
        dblist = self.mongoClient.list_database_names()
        return dblist

    def create_collection(self, database_name: str, collection_name: str):
        """creates a mongodb collection to the given database name.

        Args:
            database_name (str): name of the database
            collection_name (str): name of the collection
        """
        mydb = self.mongoClient[database_name]
        collection_list = mydb.list_collection_names()
        if collection_name in collection_list:
            print(f"collection {collection_name} had been created.")
        else:
            mycol = self.mongoClient[database_name].create_collection(collection_name)
    
    def get_collection(self, database_name: str, collection_name: str):
        """returns the collection object based on given database and collection 
        name.

        Args:
            database_name (str): database name
            collection_name (str): collection name

        Returns:
            [type]: [description]
        """
        return self.mongoClient[database_name][collection_name]

    
    
def main():
    pass


if __name__ == "__main__":
    main()