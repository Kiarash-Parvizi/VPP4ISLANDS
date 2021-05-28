import json
from src.vppNode.Optimizer import Optimizer
from .test_VppInterface import *
import pprint
import os
# import pyperclip
# from src.Models.Models import VppNodeModel

# init
optimizer = Optimizer(interf)
outputFileName = 'output/test_Optimizer.json'

#test
if __name__ == '__main__':
    optimizer.optimize()
    optimizer.distribute_results()
    # data = interf.get_graph_asJson()
    if input('dump data in output/test_Optimizer.json (yes/no): ').lower()[0] == 'y':
        os.makedirs(os.path.dirname(outputFileName), exist_ok=True)
        with open(outputFileName, 'w') as fp:
            json.dump(vppNode.to_dict(), fp=fp, indent=4, sort_keys=True)
    else:
        print('ok then')
        # print(data)
    # pyperclip.copy(data)
    
    # model = VppNodeModel()
    # model.insert_vppnode(vppNode)