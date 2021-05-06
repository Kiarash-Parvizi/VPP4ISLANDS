
from .VppNode import VppNode


class DB_Manager:
    def DB_Manager(self, vppNode: VppNode):
        self.timeIdx = 0

    def save(self) -> int:
        self.timeIdx += 1
        return self.timeIdx