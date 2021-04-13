print("importing test files..")
from src.vppNode.GraphVisualizer import GraphVisualizer
from src.vppNode.VppNode import *

print("test1...")

vppNode = VppNode()
junction = Junction()
jId0 = vppNode.add_junction(junction)
jId1 = vppNode.add_junction(junction)
jId2 = vppNode.add_junction(junction)
jId3 = vppNode.add_junction(junction)
jId4 = vppNode.add_junction(junction)
print('jId0:', jId0)
print('jId0:', jId1)

eId0 = vppNode.add_edge((jId0, jId1))
eId0 = vppNode.add_edge((jId1, jId2))
eId0 = vppNode.add_edge((jId2, jId3))
eId0 = vppNode.add_edge((jId2, jId4))
print('\teId0:', eId0)

visualizer = GraphVisualizer(vppNode)
visualizer.draw()


### change graph

