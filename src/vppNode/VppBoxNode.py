from typing import List
from .Junction import Junction
import socket


class VppBoxNode(Junction):
    # instance variables
    # ip: str
    # port: int
    ###
    def __init__(self, edges: List[int], ip: str, port: int) -> None:
        super().__init__(edges)
        self.ip = ip; self.port = port
    
    def update_data(self) -> None:
        req = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(bin(req))
            data = s.recv(1024)
        ###
        # update here
        ###
