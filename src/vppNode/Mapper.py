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
    
    def rem(self, id: int) -> bool:
        if id in self.mp:
            del self.mp[id]
            return True
        return False

    def contains(self, id: int) -> bool:
        return id in self.mp

    def getItems(self) -> AbstractSet[Tuple[int, T]]:
        return self.mp.items()
    
    def get(self, id: int) -> T:
        if self.contains(id):
            return self.mp[id]
        return None
