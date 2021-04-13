print("importing test files..")
from src.vppNode.VppNode import *

print("test1...")

vppNode = VppNode()
junction = Junction()
jId0 = vppNode.add_junction(junction)
jId1 = vppNode.add_junction(junction)
print('jId0:', jId0)
print('jId0:', jId1)

eId0 = vppNode.add_edge((1, 2))
print('\teId0:', eId0)