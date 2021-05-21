import pprint
from src.vppNode.VppInterface import VppInterface

from .test_15bus import *

# init
interf = VppInterface(vppNode)

#test
if __name__ == '__main__':
    dat = interf.get_optimizer_input_data()
    pprint.pprint(dat)