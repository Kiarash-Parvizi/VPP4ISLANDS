import json
from src.vppNode.Optimizer import Optimizer
from .test_VppInterface import *
import pprint
# import pyperclip
# from src.Models.Models import VppNodeModel

# init
optimizer = Optimizer(interf)

#test
if __name__ == '__main__':
    optimizer.optimize()
    optimizer.distribute_results()
    # data = interf.get_graph_asJson()
    if input('print data here: ').lower()[0] == 'y':
        with open('test.json', 'w') as fp:
            json.dump(vppNode.to_dict(), fp)
        # print(data)
    # pyperclip.copy(data)
    
    # model = VppNodeModel()
    # model.insert_vppnode(vppNode)