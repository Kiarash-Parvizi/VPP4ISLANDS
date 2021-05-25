from src.vppNode.Optimizer import Optimizer
from .test_VppInterface import *
import pprint
import pyperclip

# init
optimizer = Optimizer(interf)

#test
if __name__ == '__main__':
    optimizer.optimize()
    optimizer.distribute_results()
    data = interf.get_graph_asJson()
    if input('print data here: ').lower()[0] == 'y':
        print(data)
    pyperclip.copy(data)
    pass
