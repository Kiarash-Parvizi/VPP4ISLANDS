print("importing test files..")
from src.vppNode.GraphVisualizer import GraphVisualizer
from src.vppNode.VppNode import *

print("test1...")

vppNode = VppNode()
junction_objs = [Junction() for _ in range(20)]
jId1 = vppNode.add_junction(junction_objs[0])
jId2 = vppNode.add_junction(junction_objs[1])
jId3 = vppNode.add_junction(junction_objs[2])
jId4 = vppNode.add_junction(junction_objs[3])
jId5 = vppNode.add_junction(junction_objs[4])
print('jId1:', jId1)
print('jId2:', jId2)

lineProps = LineProps(0, 0, 0, 0)
eId1 = vppNode.add_edge((jId1, jId2), lineProps)
eId2 = vppNode.add_edge((jId2, jId3), lineProps)
eId3 = vppNode.add_edge((jId3, jId4), lineProps)
eId4 = vppNode.add_edge((jId3, jId5), lineProps)
print('\teId1:', eId1)

visualizer = GraphVisualizer(vppNode)
#visualizer.draw()


### change graph

r0 = vppNode.rem_edge(eId2)
print('r0:', r0)

visualizer.process()
#visualizer.draw()

# add more items
jId6 = vppNode.add_junction(junction_objs[5])
jId7 = vppNode.add_junction(junction_objs[6])
jId8 = vppNode.add_junction(junction_objs[7])
jId9 = vppNode.add_junction(junction_objs[8])

eId5 = vppNode.add_edge((jId2, jId6), lineProps)
eId6 = vppNode.add_edge((jId2, jId7), lineProps)
eId7 = vppNode.add_edge((jId1, jId8), lineProps)
eId8 = vppNode.add_edge((jId1, jId9), lineProps)

visualizer.process()
visualizer.draw()

# remove junction
r1 = vppNode.rem_junction(jId1)
print('r1:', r1)

visualizer.process()
visualizer.draw()

r2 = vppNode.rem_edge(eId3)
print('r2:', r2)

visualizer.process()
visualizer.draw()

# make a triangle

eId6 = vppNode.add_edge((jId4, jId8), lineProps)
eId7 = vppNode.add_edge((jId8, jId9), lineProps)
eId8 = vppNode.add_edge((jId9, jId4), lineProps)

visualizer.process()
visualizer.draw()

# clear everything:
vppNode.clear()

jId10 = vppNode.add_junction(junction_objs[9])
jId11 = vppNode.add_junction(junction_objs[10])
eid = vppNode.add_edge((jId10, jId11), lineProps)

visualizer.process()
visualizer.draw()
