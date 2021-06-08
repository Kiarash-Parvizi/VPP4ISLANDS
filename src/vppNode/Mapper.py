from typing import AbstractSet, Generic, Mapping, Tuple, TypeVar

T = TypeVar('T')

class Mapper(Generic[T]):
    # instance variables
    # counter: int = 0
    # mp: Mapping[int, T]
    ###
    def __init__(self) -> None:
        self.counter = 0
        self.mp: Mapping[int, T] = {}

    def add(self, obj: T) -> int:
        self.counter += 1
        self.mp[self.counter] = obj
        return self.counter
    
    def add_by_id(self, id: int, obj: T) -> None:
        self.mp[id] = obj

    def is_empty(self):
        if self.mp:
            return False
        return True
    
    def rem(self, id: int) -> bool:
        if id in self.mp:
            del self.mp[id]
            return True
        return False

    def contains(self, id: int) -> bool:
        return id in self.mp
    
    def len(self) -> int:
        return len(self.mp)

    def getItems(self) -> AbstractSet[Tuple[int, T]]:
        return self.mp.items()
    
    def get(self, id: int) -> T:
        if self.contains(id):
            return self.mp[id]
        return None

    def to_dict(self) -> dict:
        obj = {}
        obj['counter'] = self.counter
        obj['mp'] = {}
        for key, value in self.mp.items():
            obj['mp'][key] = value.to_dict()
        return obj
    
    @staticmethod
    def create_from_dict(_dict: dict, _obj):
        obj = Mapper[T]()
        obj.counter = _dict['counter']
        for key, value in _dict['mp'].items():
            obj.mp[key] = _obj.create_from_dict(value)
        return obj